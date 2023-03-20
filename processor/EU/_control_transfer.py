import datetime

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
        self.write_memory(self.physical_sp, self.read_register('IP'))
        self.instruction = 'JMP'
        self.execute()
    
    elif (self.instruction in ['RET', 'RETN']):
        self.write_register('IP', self.read_memory(self.physical_sp))
        self.increment_register('SP', 2)
    
    elif (self.instruction == 'RETF'):
        self.write_register('IP', self.read_memory(self.physical_sp))
        self.increment_register('SP', 2)
        self.write_register('CS', self.read_memory(self.physical_sp))
        self.increment_register('SP', 2)

    # Iteration Control
    elif (self.instruction == 'LOOP'):
        self.increment_register('CX', -1)
        if (self.gpr['CX'] != 0):
            self.write_register('IP', self.fetch_operand(self.operands[0]))

    elif (self.instruction in ['LOOPE', 'LOOPZ']):
        self.increment_register('CX', -1)
        if (self.gpr['CX'] != 0 and self.flag.zero == 1):
            self.write_register('IP', self.fetch_operand(self.operands[0]))
    
    elif (self.instruction in ['LOOPNE', 'LOOPNZ']):
        self.increment_register('CX', -1)
        if (self.gpr['CX'] != 0 and self.flag.zero == 0):
            self.write_register('IP', self.fetch_operand(self.operands[0]))

    elif (self.instruction == 'JCXZ'):
        if (self.gpr['CX'] == 0):
            self.write_register('IP', self.fetch_operand(self.operands[0]))

    elif (self.instruction in instructions.conditional_transfer):
        jump_hash = {
            'JA':   self.flag.carry == 0 and self.flag.zero == 0,
            'JAE':  self.flag.carry == 0,
            'JB':   self.flag.carry == 1,
            'JBE':  self.flag.carry == 0 and self.flag.zero == 1,
            'JC':   self.flag.carry == 1,
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
    
    # Interrupts
    elif (self.instruction == 'INT'):
        if not self.operands:
            self.print("\breakpoint interrupt\n")
            self.interrupt = True
        else:
            int_type = utils.decimal(self.operands[0])
            if int_type == 3: # breakpoint
                self.print("\breakpoint interrupt\n")
                self.interrupt = True
            elif int_type == utils.decimal('10H'):
                self.bios_isr_10h()
            elif int_type == utils.decimal('21H'):
                ah = self.read_register('AH')
                al = self.read_register('AL')
                if self.debug_interrupts:
                    self.print(f"\nCall DOS interrupt routine 21H, AH={hex(ah)}\n")
                
                if ah == 0x0:
                    if self.debug_interrupts:
                        self.print("Interrupt Routine Function: Program Termination\n")
                    self.print("> " * 16 + "Exit to operating system")
                    self.shutdown = True

                elif ah == 0x01:
                    if self.debug_interrupts:
                        self.print("Interrupt routine function: keyboard typing and echoing\n")
                    char = input()[0]
                    self.write_register('AL', ord(char)) # ascii存储
                
                elif ah == 0x02:
                    if self.debug_interrupts:
                        self.print("Interrupt routine function: display output\n")
                    char = chr(self.read_register('DL'))
                    self.print('> '+ char + '\n')

                elif ah == 0x9: # Display string DS:DX= string address '$' end string
                    if self.debug_interrupts:
                        self.print("Interrupt routine function: display string\n")
                    address = (self.read_register('DS') << 4) + self.read_register('DX')
                    count = 0

                    while True:
                        char = chr(utils.decimal(self.bus.read_byte(address)[0]))
                        if char == '$' or count == 500: # If it does not end, it stops when it reaches the 500 cap.
                            break
                        # print(address)
                        self.print(char)
                        address += 1
                        count += 1

                elif ah == 0x2a: # Get date: CX:DH:DL = year:month:day
                    if self.debug_interrupts:
                        self.print("Interrupt routine function: read system date\n")
                    now = datetime.datetime.now()
                    self.write_register('CX', now.year)
                    self.write_register('DH', now.month)
                    self.write_register('DL', now.day)

                elif ah == 0x2c: # Get time: CH:CL = hour:minute DH:DL = second:millisecond
                    if self.debug_interrupts:
                        self.print("Interrupt routine function: read system time\n")
                    now = datetime.datetime.now()
                    self.write_register('CH', now.hour)
                    self.write_register('CL', now.minute)
                    self.write_register('DH', now.second)
                    self.write_register('DL', int(now.microsecond * 1e4))
                
                elif ah == 0x35:
                    if self.debug_interrupts:
                        self.print("Interrupt routine function: fetch interrupt vector\n")
                    int_type = self.read_reg('AL')
                    self.write_register('BX', self.read_memory(int_type * 4))
                    self.write_register('ES', self.read_memory(int_type * 4 + 2))
                
                elif ah == 0x4c: # Exit with return code
                    if self.debug_interrupts:
                        self.print("Interrupt routine function: end with return value\n")
                    self.print(f"\nExit with return code {al}\n")
                    self.shutdown = True
                else:
                    raise SyntaxError('Interrupt Error')
            elif int_type in [utils.decimal(i) for i in ['7ch']]:
                self.interrupt_handler(int_type)
            else:
                raise SyntaxError('Interrupt Error')