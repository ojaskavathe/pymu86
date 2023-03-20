from processor.memory import Memory
from processor.biu import BIU
from processor.EU import EU

class CPU:

    def __init__(
        self,
        memory: Memory,
        debug: bool
    ) -> None:
        self.num_cycles: int = 0
        self.biu = BIU(6, memory)
        self.eu = EU(self.biu, debug)
        pass

    def run(self):
        self.biu.run()
        self.eu.run()

    def terminated(self) -> bool:
        if (self.eu.interrupt or self.eu.shutdown):
            return True
        
        return (self.biu.instruction_queue.empty() and self.biu.instructions_done())

    def print_end_state(self):
        # print end status
        self.eu.print("Clock ended\n")

        