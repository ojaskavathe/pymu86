from processor.biu import BIU
from processor.flag import FlagRegister
from statements import instructions
from src import utils

from ._data_transfer import data_transfer
from ._arithmetic import arithmetic
from ._bit_manipulation import bit_manipulation
from ._string import string
from ._control_transfer import control_transfer

class EU:

    def __init__(
        self,
        bus: BIU,
        debug: bool
    ) -> None:
        self.bus = bus
        self.IR: list[str] = []
        self.flag: FlagRegister = FlagRegister()
        self.gpr: dict[str] = {
            'AX': 0,    # data
            'BX': 0,
            'CX': 0,
            'DX': 0,
            'SP': 0,    # pointer
            'BP': 0,
            'SI': 0,    # index
            'DI': 0,
        }
        self.gpr_half: list[str] = ['AH', 'AL', 'BH', 'BL', 'CH', 'CL', 'DH', 'DL']
        self.gpr_all: list[str] = [reg for reg in self.gpr] + self.gpr_half
        self.bus_reg: list[str] = [reg for reg in self.bus.registers]

        self.interrupt: bool = debug
        self.debug_interrupts: bool = False

        self.shutdown = False

        self.instruction: str = ''
        self.operands: list[str] = []
        self.operand_size: int = 2               # size of operands in bytes

        self.output: str = ''

    def run(self) -> None:
        self.operands = []
        self.IR = self.bus.instruction_queue.get()
        self.instruction = self.IR[0]
        self.bus.registers['IP'] += 1
        self.operands = self.IR[1:]
        self.fetch_operand_size()
        self.execute()
        pass

    def execute(self) -> None:
        cs_start_ip = self.bus.phy_ip
        if(self.instruction in instructions.data_transfer):
            data_transfer(self)
        elif(self.instruction in instructions.arithmetic):
            arithmetic(self)
        elif(self.instruction in instructions.bit_manipulation):
            bit_manipulation(self)
        elif(self.instruction in instructions.string):
            string(self)
        elif(self.instruction in instructions.control_transfer):
            control_transfer(self)
        else:
            raise SyntaxError('Instruction[' + self.instruction + '] not supported.')

        if (cs_start_ip != self.bus.phy_ip):
            self.bus.clear_instruction_queue()

    def fetch_operand_size(self) -> None:
        self.operand_size = 2
        for operand in self.operands:
            if (operand in self.gpr_half):
                self.operand_size = 1

        if ('PTR' in self.operands):
            self.operands.remove('PTR')
            if ('BYTE' in self.operands):
                self.operand_size = 1
                self.operands.remove('BYTE')
            elif ('WORD' in self.operands):
                self.operand_size = 2
                self.operands.remove('WORD')
            elif ('DWORD' in self.operands):
                self.operand_size = 4
                self.operands.remove('DWORD')
            else:
                raise SyntaxError('No Field Value for PTR.')
        
        if self.instruction in instructions.string:
            if ('B' in self.instruction):
                self.operand_size = 1
            else:
                self.operand_size = 2

    def read_register(
        self,
        register: str
    ) -> int:
        if (register in self.gpr):
            return self.gpr[register]
        elif (register in self.gpr_half):
            if(register[1] == 'L'):
                full_reg = register[0] + 'X'
                return (self.gpr[full_reg] & 0xff)
            elif (register[1] == 'H'):
                full_reg = register[0] + 'X'
                return ((self.gpr[full_reg] >> 8) & 0xff)
        elif (register in self.bus_reg):
            return self.bus.registers[register]
        else:
            raise SyntaxError('Register not recognized: ' + register)
        
    def write_register(
        self,
        register: str,
        value: int
    ) -> None:
        value = utils.unsigned(value, self.operand_size) & 0xffff       # anding so num fits in 2 bytes
        if (register in self.gpr):
            self.gpr[register] = value

        elif (register in self.gpr_half):
            if(register[1] == 'L'):
                full_reg = register[0] + 'X'
                self.gpr[full_reg] = (self.gpr[full_reg] & 0xff00) + (value & 0xff)
            elif (register[1] == 'H'):
                full_reg = register[0] + 'X'
                self.gpr[full_reg] = (self.gpr[full_reg] & 0x00ff) + ((value << 8) & 0xff00)

        elif (register in self.bus_reg):
            self.bus.registers[register] = value

        else:
            raise SyntaxError('Register not recognized: ' + register)

    def increment_register(
        self,
        register: str,
        value: int
    ) -> None:
        self.write_register(register, self.read_register(register) + value)

    def fetch_address(
        self,
        operand: str
    ) -> int:
        out = 0

        address_reg = ['BX', 'BP', 'SI', 'DI']
        segment_reg = ['CS', 'DS', 'SS', 'ES']
        has_segments = False

        addresses = utils.split_words(operand)

        for address in addresses:
            if (address in address_reg):
                out += self.read_register(address)
            elif (address in segment_reg):
                out += (self.read_register(address) << 4)
                has_segments = True
            else:
                out += utils.decimal(address)

        if (not has_segments):
            if ('BP' in addresses):     # BP addresses the stack unless specified otherwise 
                out += (self.read_register('SS') << 4)
            else:
                out += (self.read_register('DS') << 4)

        return out

    def read_memory(
        self,
        address: int
    ) -> int:
        if(self.operand_size == 1):
            result = self.bus.read_byte(address)
        elif(self.operand_size == 2):
            result = self.bus.read_word(address)
        elif(self.operand_size == 4):
            result = self.bus.read_dword(address)
        else:
            raise SyntaxError('Could not read from location ' + address)

        out = 0
        for res in result:
            out = (out << 8) + (int(res, 16) & 0xff)
        return out

    def write_memory(
        self,
        address: int,
        data: str
    ) -> None:
        if(self.operand_size == 1):
            self.bus.write_byte(address, data)
        elif(self.operand_size == 2):
            self.bus.write_word(address, data)
        elif(self.operand_size == 4):
            self.bus.write_dword(address, data)
        else:
            raise SyntaxError('Could not write (' + data + ') to location ' + address)

    def fetch_operand(
        self,
        operand: str | int
    ) -> int:
        if(isinstance(operand, int)):   # when called from within eu, and not from an asm string 
            operand = '[' + str(operand) + ']'
        
        if(operand in (self.gpr_all + self.bus_reg)):   # register
            return self.read_register(operand)
        elif('[' in operand):                           # indirect, base, indexed etc
            address = self.fetch_address(operand)
            if(self.operand_size == 1):
                result = self.bus.read_byte(address)
            elif(self.operand_size == 2):
                result = self.bus.read_word(address)
            elif(self.operand_size == 4):
                result = self.bus.read_dword(address)
            else:
                raise SyntaxError('Could not fetch operand: ' + operand)
            
            out = 0
            for res in result:
                out = (out << 8) + (int(res, 16) & 0xff)
            return out
        elif (operand[0] == operand[-1] == '\''):
            return ord(operand[1])
        else:                                           # immediate
            return utils.decimal(operand)
        
    def write_operand(
        self,
        operand: str,
        data: int
    ) -> None:
        if (self.is_address(operand)):
            address = self.fetch_address(operand)
            self.write_memory(address, data)
        elif (self.is_register(operand)):
            self.write_register(operand, data)
    
    def print(self, string):
        """Prints emulator output."""
        print(string, end='')

        self.output += string
    
    @property
    def physical_sp(self) -> int:
        return ( (self.bus.registers['SS'] * 16) + self.gpr['SP'] )
    
    def is_register(
        self,
        string: str
    ) -> bool:
        return string in (self.gpr_all + self.bus_reg)
    
    def is_address(
        self,
        string: str
    ) -> bool:
        return '[' in string
    
    def interrupt_handler(
        self,
        type: int
    ):
        self.increment_register('SP', -2)
        self.write_memory(self.physical_sp, self.flag.get())
        self.flag.trap = 0
        self.flag.interrupt = 0
        self.increment_register('SP', -2)
        self.write_memory(self.physical_sp, self.read_register('CS'))
        self.increment_register('SP', -2)
        self.write_memory(self.physical_sp, self.read_register('IP'))
        self.operand_size = 2
        ip_val = self.read_memory(type * 4)
        cs_val = self.read_memory(type * 4 + 2)
        self.write_register('IP', ip_val)
        self.write_register('CS', cs_val)
        if self.debug_interrupts:
            self.print(f"Execute interrupt: {hex(type)} ...\n")
            self.print("Securing Site Success\n")
            self.print(f"Read interrupt vector table {hex(type * 4)} offset address {hex(ip_val)} => IP\n")
            self.print(f"Read interrupt vector table {hex(type * 4 + 2)} Branch address {hex(cs_val)} => CS\n")
            self.print("Enter the interrupt routine...\n")