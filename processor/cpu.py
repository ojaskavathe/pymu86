from processor.memory import Memory
from processor.biu import BIU
from processor.EU import EU

class CPU:

    def __init__(
        self,
        memory: Memory
    ) -> None:
        self.num_cycles: int = 0
        self.biu = BIU(6, memory)
        self.eu = EU(self.biu)
        pass

    def run(self):
        self.biu.run()
        self.eu.run()

        