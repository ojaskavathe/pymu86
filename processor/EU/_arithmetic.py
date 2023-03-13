from src import utils

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from processor.EU import EU

def arithmetic(self: "EU") -> None:
    # Addition
    if (self.instruction == 'ADD'):
        a = self.fetch_operand(self.operands[0])
        b = self.fetch_operand(self.operands[1])
        res = (a + b) & int('0x' + 'f' * self.operand_size * 2, 16)
        
        self.write_operand(self.operands[0], res)

        self.flag.set_overflow(a + b, self.operand_size)
        self.flag.set_carry( ( (utils.unsigned(a, self.operand_size) + \
                                utils.unsigned(b, self.operand_size)) \
                                    >> (self.operand_size * 8) ) > 0 )
        self.flag.set_parity(res)
        self.flag.set_zero(res)
        self.flag.set_sign(res, self.operand_size)

    elif (self.instruction == 'ADC'):
        a = self.fetch_operand(self.operands[0])
        b = self.fetch_operand(self.operands[1])
        res = (a + b + self.flag.carry) & int('0x' + 'f' * self.operand_size * 2, 16)
        
        self.write_operand(self.operands[0], res)

        self.flag.set_overflow(a + b + self.flag.carry, self.operand_size)
        self.flag.set_carry( ( (utils.unsigned(a, self.operand_size) + \
                                utils.unsigned(b, self.operand_size) + \
                                self.flag.carry) >> (self.operand_size * 8) ) > 0 )
        self.flag.set_parity(res)
        self.flag.set_zero(res)
        self.flag.set_sign(res, self.operand_size)

    elif (self.instruction == 'INC'):
        src = self.fetch_operand(self.operands[0])
        res = (src + 1) & int('0x' + 'f' * self.operand_size * 2, 16)
        
        self.write_operand(self.operands[0], res)

        self.flag.set_overflow(src + 1, self.operand_size)
        self.flag.set_parity(res)
        self.flag.set_zero(res)
        self.flag.set_sign(res, self.operand_size)

    elif (self.instruction == 'AAA'):
        pass

    elif (self.instruction == 'DAA'):
        pass

    # Subtraction
    elif (self.instruction == 'SUB'):
        a = self.fetch_operand(self.operands[0])
        b = self.fetch_operand(self.operands[1])
        res = (a - b) & int('0x' + 'f' * self.operand_size * 2, 16)
        
        self.write_operand(self.operands[0], res)

        self.flag.set_overflow(a - b, self.operand_size)
        self.flag.set_carry(utils.unsigned(a, self.operand_size) < utils.unsigned(b, self.operand_size))
        self.flag.set_parity(res)
        self.flag.set_zero(res)
        self.flag.set_sign(res, self.operand_size)

    elif (self.instruction == 'SBB'):
        a = self.fetch_operand(self.operands[0])
        b = self.fetch_operand(self.operands[1])
        res = (a - b - self.flag.carry) & int('0x' + 'f' * self.operand_size * 2, 16)
        
        self.write_operand(self.operands[0], res)

        self.flag.set_overflow(a - b - self.flag.carry, self.operand_size)
        c = utils.unsigned(a, self.operand_size) < (utils.unsigned(b, self.operand_size) + self.flag.carry)
        self.flag.set_carry(c)
        self.flag.set_parity(res)
        self.flag.set_zero(res)
        self.flag.set_sign(res, self.operand_size)

    elif (self.instruction == 'DEC'):
        src = self.fetch_operand(self.operands[0])
        res = (src - 1) & int('0x' + 'f' * self.operand_size * 2, 16)
        
        self.write_operand(self.operands[0], res)

        self.flag.set_overflow(src - 1, self.operand_size)
        self.flag.set_parity(res)
        self.flag.set_zero(res)
        self.flag.set_sign(res, self.operand_size)

    elif (self.instruction == 'NEG'):
        src = self.fetch_operand(self.operands[0])
        res = ((~src) + 1) & int('0x' + 'f' * self.operand_size * 2, 16)    # 2's complement

        self.write_operand(self.operands[0], res)

        self.flag.set_overflow((~src) + 1, self.operand_size)
        self.flag.set_carry( (utils.unsigned(((~src) + 1), self.operand_size) >> (self.operand_size * 8) ) > 0 )
        self.flag.set_parity(res)
        self.flag.set_zero(res)
        self.flag.set_sign(res, self.operand_size)

    elif (self.instruction == 'CMP'):
        a = self.fetch_operand(self.operands[0])
        b = self.fetch_operand(self.operands[1])
        res = (a - b) & int('0x' + 'f' * self.operand_size * 2, 16)
        
        self.flag.set_overflow(a - b, self.operand_size)
        self.flag.set_carry(utils.unsigned(a, self.operand_size) < utils.unsigned(b, self.operand_size))
        self.flag.set_parity(res)
        self.flag.set_zero(res)
        self.flag.set_sign(res, self.operand_size)

    elif (self.instruction == 'AAS'):
        pass

    elif (self.instruction == 'AAS'):
        pass

    # Multiplication
    elif (self.instruction == 'MUL'):
        if(self.operand_size not in [1, 2]):
            raise SyntaxError('Operands in MUL have can\'t have size > 2')
        
        b = utils.unsigned(self.fetch_operand(self.operands[0]), self.operand_size)
        if (self.operand_size == 1):
            a = utils.unsigned(self.read_register('AL'), 1)
            self.write_register('AX', a * b)
            if (self.read_register('AH') > 0):
                self.flag.overflow = self.flag.carry = 1
            else:
                self.flag.overflow = self.flag.carry = 0
        elif (self.operand_size == 2):
            a = utils.unsigned(self.read_register('AX'), 2)
            res = a * b
            self.write_register('AX', (res & 0xffff))
            self.write_register('DX', ((res >> 16) & 0xffff))

    elif (self.instruction == 'IMUL'):
        if(self.operand_size not in [1, 2]):
            raise SyntaxError('Operands in MUL have can\'t have size > 2')
        
        b = utils.signed(self.fetch_operand(self.operands[0]), self.operand_size)
        if (self.operand_size == 1):
            a = utils.signed(self.read_register('AL'), 1)
            self.write_register('AX', a * b)
            if (self.read_register('AH') > 0):
                self.flag.overflow = self.flag.carry = 1
            else:
                self.flag.overflow = self.flag.carry = 0
        elif (self.operand_size == 2):
            a = utils.signed(self.read_register('AX'), 2)
            res = a * b
            self.write_register('AX', (res & 0xffff))
            self.write_register('DX', ((res >> 16) & 0xffff))

    elif (self.instruction == 'AAM'):
        pass

    # Division
    elif (self.instruction == 'DIV'):
        if(self.operand_size not in [1, 2]):
            raise SyntaxError('Operands in DIV have can\'t have size > 2')
        
        b = utils.unsigned(self.fetch_operand(self.operands[0]), self.operand_size)
        if(b == 0):
            raise SyntaxError('Division by zero')
        if (self.operand_size == 1):
            a = utils.unsigned(self.read_register('AL'), 1)
            self.write_register('AL', a // b)
            self.write_register('AH', a % b)
        elif (self.operand_size == 2):
            a = (utils.unsigned(self.read_register('DX'), 2) << 16) + \
                (utils.unsigned(self.read_register('AX'), 2))
            self.write_register('AX', ((a // b) & 0xffff))
            self.write_register('DX', ((a % b)  & 0xffff))

    elif (self.instruction == 'IDIV'):
        if(self.operand_size not in [1, 2]):
            raise SyntaxError('Operands in DIV have can\'t have size > 2')
        
        b = utils.signed(self.fetch_operand(self.operands[0]), self.operand_size)
        if(b == 0):
            raise SyntaxError('Division by zero')
        if (self.operand_size == 1):
            a = utils.signed(self.read_register('AL'), 1)
            self.write_register('AL', a // b)
            self.write_register('AH', a % b)
        elif (self.operand_size == 2):
            a = (utils.signed(self.read_register('DX'), 2) << 16) + \
                (utils.signed(self.read_register('AX'), 2))
            self.write_register('AX', ((a // b) & 0xffff))
            self.write_register('DX', ((a % b)  & 0xffff))
    
    elif (self.instruction == 'AAD'):
        pass

    elif (self.instruction == 'CBW'):
        src = self.read_register('AL')
        self.write_register('AH', 255 * ((src >> 7) & 1))       # 0 if al is +ve, ff if -ve

    elif (self.instruction == 'CWD'):
        src = self.read_register('AX')
        self.write_register('DX', 65535 * ((src >> 15) & 1))    # 0 if ax is +ve, ffff if -ve

    