from processor.biu import BIU
from processor.flag import FlagRegister
from statements import instructions
from src import utils

class EU:

    def __init__(
        self,
        bus: BIU
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
        self.gpr_half = ['AH', 'AL', 'BH', 'BL', 'CH', 'CL', 'DH', 'DL']
        self.gpr_all = [reg for reg in self.gpr] + self.gpr_half
        self.bus_reg = [reg for reg in self.bus.registers]

        self.instruction: str = ''
        self.operands: list[str] = []
        self.operand_size: int = 2               # size of operands in bytes

        self.output = ''

    def run(self) -> None:
        self.operands = []
        self.IR = self.bus.instruction_queue.get()
        self.instruction = self.IR[0]
        self.operands = self.IR[1:]
        self.fetch_operand_size()
        self.execute()
        pass

    def execute(self) -> None:
        cs_start_ip = self.bus.seg_start_ip('CS')
        if(self.instruction in instructions.data_transfer):
            self.data_transfer()
        elif(self.instruction in instructions.arithmetic):
            self.arithmetic()

    def data_transfer(self) -> None:
        if(self.instruction == 'MOV'):
            source = self.fetch_operand(self.operands[1])
            self.write_operand(self.operands[0], source)

        if(self.instruction == 'PUSH'):
            source = self.fetch_operand(self.operands[0])
            self.increment_register('SP', -2)
            self.write_memory(self.effective_sp, source)

        if(self.instruction == 'POP'):
            popped = self.bus.read_word(self.effective_sp)
            source = 0
            for n in popped:
                source = (source << 8) + int(n, 16)

            dest = self.operands[0]
            if (self.is_address(dest)):
                self.write_memory(self.fetch_address(dest), source)
            elif (self.is_register(dest)):
                self.write_register(dest, source)
            
            self.increment_register('SP', 2)

        elif(self.instruction == 'XLAT'):
            pass

        # I/O
        elif(self.instruction == 'IN'):
            # Input from port into AL or AX. IN AX, 4; IN AL, 7;
            # And we are not restricted to AL and AX, you can input to all regs.
            port = utils.decimal(self.operands[1])
            val = utils.decimal(input(f"Input to Port {port}: "))
            self.write_register(self.operands[0], val)

        elif self.instruction == 'OUT':
            # Output from AL or AX to port. OUT 4, AX; OUT DX, AX
            # And we are not restricted to AL and AX, you can output from all regs.
            # If port > 255, use DX.
            port = utils.decimal(self.operands[0])
            val = self.read_register(self.operands[1])
            self.print("> " * 16 + "@Port {}: 0x{:<4x} => {}\n".format(port, val, val))

        elif(self.instruction == 'XCHG'):
            a = self.fetch_operand(self.operands[0])
            b = self.fetch_operand(self.operands[1])
            self.write_operand(self.operands[0], b)
            self.write_operand(self.operands[1], a)


    def arithmetic(self) -> None:
        if (self.instruction == 'ADD'):
            a = self.fetch_operand(self.operands[0])
            b = self.fetch_operand(self.operands[1])
            res = (a + b) & int('0x' + 'f' * self.operand_size * 2, 16)

    def fetch_operand_size(self) -> None:
        self.operand_size = 2
        for operand in self.operands:
            if (operand in self.gpr_half):
                self.operand_size = 1

        if 'PTR' in self.operands:
            self.operands.remove('PTR')
            if ('BYTE' in self.operands):
                self.operand_size = 1
                self.operands.remove('PTR')
            elif ('WORD' in self.operands):
                self.operand_size = 1
                self.operands.remove('WORD')
            elif ('DWORD' in self.operands):
                self.operand_size = 1
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
        value = utils.unsigned(value, self.operand_size) & 0xffff       # anding so num fits in 4 bytes
        if (register in self.gpr):
            self.gpr[register] = value
        elif (register in self.gpr_half):
            if(register[1] == 'L'):
                full_reg = register[0] + 'X'
                self.gpr[full_reg] = (self.gpr[full_reg] & 0xff00) + (value & 0xff)
            elif (register[1] == 'H'):
                full_reg = register[0] + 'X'
                self.gpr[full_reg] = (self.gpr[full_reg] & 0xff) + (value << 8)
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

    def write_memory(
        self,
        address: int,
        data: str
    ) -> None:
        if(self.operand_size == 1):
            self.bus.write_byte(address)
        elif(self.operand_size == 2):
            self.bus.write_word(address)
        elif(self.operand_size == 4):
            self.bus.write_dword(address)
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
    def effective_sp(self) -> int:
        return (self.bus.registers['SS'] + self.gpr['SP'])
    
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