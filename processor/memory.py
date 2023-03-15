from src.executable import Executable
from processor.ICU import interrupt_controller

class Memory:

    def __init__(
        self,
        segment_size: int,
        memory_size: int
    ) -> None:
        self.memory_size: int       = memory_size
        self.segment_size: int      = segment_size
        self.space: list[list[str]] = [['0']] * memory_size

    def read_byte(
        self,
        address: int
    ) -> list[str]:
        return self.space[address]

    def write_byte(
        self,
        address: int,
        data: str
    ) -> None:
        self.space[address] = [data]

    def load(
        self,
        exec: Executable,
        debug: bool
    ) -> None:
        """Loads the program executable into memory."""
        self.executable = exec

        for segment in exec.segment_space:
            segment_address  = int(exec.segment_address[segment], 16)           # '0x1000' -> 4096
            physical_address = segment_address * 16                             # '0x1000' -> '0x10000'
            segment_length   = exec.segment_lengths[segment]
            segment_end      = physical_address + segment_length                # '0x10000' + 64K
            self.space[physical_address: segment_end] = exec.segment_space[segment][:segment_length]

            # Super janky, find a better solution
            # The reason I have to do this is if two segments overlap, the overlapped region gets reset even 
            # if that region of memory isn't being used. So my solution for the time being is to only load
            # the parts of the segment that are currently being used

        interrupt_controller.load_isr(self, debug)

    def clear(self) -> None:
        """Sets all memory locations to 0."""
        self.space = [['0']] * self.memory_size

    def is_null(
        self,
        address: int
    ) -> bool:
        return (self.space[address] == ['0'])
