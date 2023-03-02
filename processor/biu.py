import queue
from src.executable import Executable
from processor.memory import Memory

class BIU:
    """The Bus Interface Unit: Gets instructions and data to and from memory"""

    def __init__(
        self, 
        queue_size: int,
        exec: Executable,
        memory: Memory
    ) -> None:
        self.instruction_queue = queue.Queue(queue_size)
        self.memory = memory

        self.reg = {
            'CS': int(exec.segment_address['CS'], 16),
            'DS': int(exec.segment_address['DS'], 16),
            'SS': int(exec.segment_address['SS'], 16),
            'ES': int(exec.segment_address['ES'], 16),
            'IP': int(exec.ip, 16)
        }

        self.prefetch_ip = int(exec.ip, 16)

    def run(self) -> None:
        """Fetch instructions and add them to the instruction queue stream IF there are more than 2 \
            instructions missing from the queue"""
        
        if(self.instruction_queue.qsize() <= self.instruction_queue.maxsize - 2):
            self.fetch_instructions()
    
    def fetch_instructions(self) -> None:
        while(self.instruction_queue.not_full):
            if(self.memory.is_null(self.prefetch_ip)):
                break
            else:
                self.fetch_next_instruction()

    def fetch_next_instruction(self) -> None:
        next_instruction = self.memory.read_byte(self.prefetch_ip)
        self.instruction_queue.put(next_instruction)
        self.prefetch_ip += 1
    