from src.executable import Executable

class Memory:

    def __init__(
        self,
        segment_size: int,
        memory_size:  int
    ) -> None:
        self.memory_size  = memory_size
        self.segment_size = segment_size
        self.space        = [0] * memory_size

    def load(
        self,
        exec: Executable
    ) -> None:
        for segment, data in exec.segment_space:
            segment_address = int(exec.segment_addresses[segment], 16)          # '0x1000' -> 16000
            segment_end     = segment_address + self.segment_size
            self.space[segment_address: segment_end]

    def clear(self) -> None:
        self.space = [0] * self.memory_size
