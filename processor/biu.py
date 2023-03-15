import queue
from src.executable import Executable
from processor.memory import Memory

class BIU:
    """The Bus Interface Unit: Gets instructions and data to and from memory"""

    def __init__(
        self, 
        queue_size: int,
        memory: Memory
    ) -> None:
        self.instruction_queue = queue.Queue(queue_size)
        self.memory = memory

        self.registers = {
            'CS': int(memory.executable.segment_address['CS'], 16),
            'DS': int(memory.executable.segment_address['DS'], 16),
            'SS': int(memory.executable.segment_address['SS'], 16),
            'ES': int(memory.executable.segment_address['ES'], 16),
            'IP': int(memory.executable.ip, 16)
        }

        self.prefetch_ip = int(self.memory.executable.ip, 16)

    @property
    def prefetch_phy_ip(self) -> int:
        return ( (self.registers['CS'] * 16) + self.prefetch_ip )
    
    @property
    def phy_ip(self) -> None:
        return ( (self.registers['CS'] * 16) + self.registers['IP'] )

    def run(self) -> None:
        """Fetch instructions and add them to the instruction queue stream IF there are more than 2 \
            instructions missing from the queue"""
        
        if(self.instruction_queue.qsize() <= self.instruction_queue.maxsize - 2):
            self.fetch_instructions()
    
    def fetch_instructions(self) -> None:
        while(not self.instruction_queue.full()):
            if(self.memory.is_null(self.prefetch_phy_ip)):
                break
            else:
                self.fetch_next_instruction()

    def fetch_next_instruction(self) -> None:
        next_instruction = self.memory.read_byte(self.prefetch_phy_ip)
        self.instruction_queue.put(next_instruction)
        self.prefetch_ip += 1

    def clear_instruction_queue(self) -> None:
        """Empties the instruction queue whenever there's a jump/branch."""
        
        self.instruction_queue.queue.clear()
        self.prefetch_ip = self.registers['IP']

    def read_byte(
        self,
        address: int
    ) -> list[str]:
        return self.memory.read_byte(address)
    
    def read_word(
        self,
        address: int
    ) -> list[list[str]]:
        return self.memory.read_byte(address + 1) + \
               self.memory.read_byte(address)
    
    def read_dword(
        self,
        address: int
    ) -> list[list[str]]:
        return self.memory.read_byte(address + 3) + \
               self.memory.read_byte(address + 2) + \
               self.memory.read_byte(address + 1) + \
               self.memory.read_byte(address)
    
    def write_byte(
        self,
        address: int,
        data: int 
    ) -> None:
        if(isinstance(data, int)):
            self.memory.write_byte(address, hex(data))
        else:
            raise SyntaxError('Value[' + data + '] could not be written.')
        
    def write_word(
        self,
        address: int,
        data: int
    ) -> None:
        if(isinstance(data, int)):
            self.write_byte(address, data & 0xff)
            self.write_byte(address + 1, (data >> 8) & 0xff)
        # elif(isinstance(data, list)):
        #     for i, item in enumerate(list):
        #         self.write_byte(address + i, [item])
        else:
            raise SyntaxError('Value[' + data + '] could not be written.')
        
    def write_dword(
        self,
        address: int,
        data: int
    ) -> None:
        if(isinstance(data, int)):
            self.write_byte(address, data & 0xff)
            self.write_byte(address + 1, (data >> 8) & 0xff)
            self.write_byte(address + 2, (data >> 16) & 0xff)
            self.write_byte(address + 3, (data >> 24) & 0xff)
        else:
            raise SyntaxError('Value[' + data + '] could not be written.')
    
    def instructions_done(self) -> bool:
        return self.memory.is_null(self.prefetch_phy_ip)