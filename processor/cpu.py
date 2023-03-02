from processor.memory import Memory

class CPU:

    def __init__(
        self,
        memory: Memory
    ) -> None:
        self.num_cycles: int = 0

        