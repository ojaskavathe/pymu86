from src import utils
from statements import instructions

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from processor.EU import EU

def control_transfer(self: "EU") -> None:

    # Unconditional Transfer
    if (self.instruction == 'JMP'):
        if (self.is_address(self.operands[0])):     # transfer address：jmp word/dword ptr [dest]
            dest = self.fetch_address(self.operands[0])
            if (self.operand_size == 4):
                self.operand_size = 2
                self.write_register('CS', self.fetch_operand(dest + 2))
            self.write_register('IP', self.fetch_operand(dest))
        elif (':' in self.operands[0]):             # long transfer：jmp cs:ip
            self.operands = [w for w in utils.re.split(r':| ', self.operands[0]) if w]
            self.write_register('CS', self.fetch_operand(self.operands[0]))
            self.write_register('IP', self.fetch_operand(self.operands[1]))
        else:                                       # short, near, register transfer: jmp ip/reg
            self.write_register('IP', self.fetch_operand(self.operands[0]))

    elif (self.instruction == 'CALL'):
        if (self.operand_size == 4):                                # push current cs
            self.increment_register('SP', -2)
            self.write_memory(self.physical_sp, self.read_register('CS'))
        self.increment_register('SP', -2)                           # push current ip
        self.write_memory(self.physical_sp, self.read_register('CS'))
        self.instruction = 'JMP'
        self.execute()
    
    elif (self.instruction == 'RET' or self.instruction == 'RETN'):
        self.write_register('IP', self.read_memory(self.physical_sp))
        self.increment_register('SP', 2)
    
    elif (self.instruction == 'RETF'):
        self.write_register('IP', self.read_memory(self.physical_sp))
        self.increment_register('SP', 2)
        self.write_register('CS', self.read_memory(self.physical_sp))
        self.increment_register('SP', 2)

    elif (self.instruction in instructions.conditional_transfer):
        jump_hash = {
            'JA':   self.flag.carry == 0 and self.flag.zero == 0,
            'JAE':  self.flag.carry == 0,
            'JB':   self.flag.carry == 1,
            'JBE':  self.flag.carry == 0 and self.flag.zero == 1,
            'JC':   self.flag.carry == 1,
            'JCXZ': self.gpr['CX'] == 0,
            'JE':   self.flag.zero == 1,
            'JG':   self.flag.zero == 0 and self.flag.sign == self.flag.overflow,
            'JGE':  self.flag.sign == self.flag.overflow,
            'JL':   self.flag.sign != self.flag.overflow,
            'JLE':  self.flag.sign != self.flag.overflow or self.flag.zero == 1,
            'JNA':  self.flag.carry == 1 or self.flag.zero == 1,
            'JNAE': self.flag.carry == 1,
            'JNB':  self.flag.carry == 0,
            'JNBE': self.flag.carry == 0 and self.flag.zero == 0,
            'JNC':  self.flag.carry == 0,
            'JNE':  self.flag.zero == 0,
            'JNG':  self.flag.zero == 1 and self.flag.sign != self.flag.overflow,
            'JNGE': self.flag.sign != self.flag.overflow,
            'JNL':  self.flag.sign == self.flag.overflow,
            'JNLE': self.flag.sign == self.flag.overflow and self.flag.zero == 0,
            'JNO':  self.flag.overflow == 0,
            'JNP':  self.flag.parity == 0,
            'JNS':  self.flag.sign == 0,
            'JNZ':  self.flag.zero == 0,
            'JO':   self.flag.overflow == 1,
            'JP':   self.flag.parity == 1,
            'JPE':  self.flag.parity == 1,
            'JPO':  self.flag.parity == 0,
            'JS':   self.flag.sign == 1,
            'JZ':   self.flag.zero == 1
        }
        if (jump_hash[self.instruction]):
            self.write_register('IP', self.fetch_operand(self.operands[0]))     # no far conditional jumps