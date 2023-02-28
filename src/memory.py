from src.executable import Executable

class Memory:

    def __init__(
        self,
        segment_size: int,
        memory_size:  int
    ) -> None:
        self.memory_size  = memory_size
        self.segment_size = segment_size
        self.space        = [['0']] * memory_size

    def load(
        self,
        exec: Executable
    ) -> None:
        """Loads the program executable into memory."""
        for segment in exec.segment_space:
            segment_address = int(exec.segment_addresses[segment], 16)          # '0x1000' -> 4096
            segment_length  = exec.segment_lengths[segment]
            segment_end     = segment_address + segment_length                  # 4096 + 64K
            self.space[segment_address: segment_end] = exec.segment_space[segment][:segment_length]

            # Super janky, find a better solution
            # The reason I have to do this is if two segments overlap, the overlapped region gets reset even 
            # if that region of memory isn't being used. So my solution for the time being is to only load
            # the parts of the segment that are currently being used

    def clear(self) -> None:
        """Sets all memory locations to 0."""
        self.space = [['0']] * self.memory_size
