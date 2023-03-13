from src import utils

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from processor.EU import EU

def bit_manipulation(self: "EU") -> None:

    # Logical
    if (self.instruction == 'NOT'):
        src = self.fetch_operand(self.operands[0])
        self.write_operand(self.operands[0], ~src)

    elif (self.instruction == 'AND'):
        dest = self.fetch_operand(self.operands[0])
        src = self.fetch_operand(self.operands[1])
        res = dest & src

        self.write_operand(self.operands[0], res)

        self.flag.set_zero(res)
        self.flag.set_parity(res)
        self.flag.set_sign(res, self.operand_size)

    elif (self.instruction == 'OR'):
        dest = self.fetch_operand(self.operands[0])
        src = self.fetch_operand(self.operands[1])
        res = dest | src

        self.write_operand(self.operands[0], res)

        self.flag.overflow = self.flag.carry = 0
        self.flag.set_zero(res)
        self.flag.set_parity(res)
        self.flag.set_sign(res, self.operand_size)

    elif (self.instruction == 'XOR'):
        dest = self.fetch_operand(self.operands[0])
        src = self.fetch_operand(self.operands[1])
        res = dest ^ src

        self.write_operand(self.operands[0], res)

        self.flag.overflow = self.flag.carry = 0
        self.flag.set_zero(res)
        self.flag.set_parity(res)
        self.flag.set_sign(res, self.operand_size)

    elif (self.instruction == 'TEST'):
        dest = self.fetch_operand(self.operands[0])
        src = self.fetch_operand(self.operands[1])
        res = dest & src

        self.flag.overflow = self.flag.carry = 0
        self.flag.set_zero(res)
        self.flag.set_parity(res)
        self.flag.set_sign(res, self.operand_size)

    # Shifts
    elif (self.instruction == 'SAL' or \
          self.instruction == 'SHL'):
        
        src = self.fetch_operand(self.operands[0])
        count = self.fetch_operand(self.operands[1])
        c = count

        while (count):
            temp = src << 1
            self.flag.carry = (temp >> (self.operand_size * 8)) & 1
            src = temp & int('1' * self.operand_size * 8, 2)
            count -= 1

        self.write_operand(self.operands[0], src)

        high = (src >> ((self.operand_size * 8) - 1)) & 1           # overflow set only if shifted ONCE
        if (c == 1):
            self.flag.overflow = int(self.flag.carry != high)
        
    elif (self.instruction == 'SHR'):
        src = self.fetch_operand(self.operands[0])
        count = self.fetch_operand(self.operands[1])

        if (count == 1):
            high = (src >> ((self.operand_size * 8) - 1)) & 1
            self.flag.overflow = high

        while (count):
            self.flag.carry = src & 1
            src = src >> 1
            count -= 1

        self.write_operand(self.operands[0], src)

    elif (self.instruction == 'SAR'):
        src = self.fetch_operand(self.operands[0])
        count = self.fetch_operand(self.operands[1])

        if (count == 1):
            self.flag.overflow = 0

        sign = (src >> ((self.operand_size * 8) - 1)) & 1
        while (count):
            self.flag.carry = src & 1
            src = (src >> 1)
            count -= 1
        src += (sign << ((self.operand_size * 8) - 1))

        self.write_operand(self.operands[0], src)

    # Rotates
    elif (self.instruction == 'ROL'):
        src = self.fetch_operand(self.operands[0])
        count = self.fetch_operand(self.operands[1])
        c = count

        while (count):
            self.flag.carry = (src >> ((self.operand_size * 8) - 1)) & 1
            src = ((src << 1) + self.flag.carry) & int('1' * self.operand_size * 8, 2)
            count -= 1

        self.write_operand(self.operands[0], src)

        high = (src >> ((self.operand_size * 8) - 1)) & 1           # overflow set only if shifted ONCE
        if (c == 1):
            self.flag.overflow = int(self.flag.carry != high)

    elif (self.instruction == 'ROR'):
        src = self.fetch_operand(self.operands[0])
        count = self.fetch_operand(self.operands[1])
        c = count

        while (count):
            self.flag.carry = src & 1
            src = (src >> 1) + (self.flag.carry << ((self.operand_size * 8) - 1))
            src = src & int('1' * self.operand_size * 8, 2)
            count -= 1

        self.write_operand(self.operands[0], src)

        if (c == 1):
            high = (src >> ((self.operand_size * 8) - 1)) & 1           # overflow set only if shifted ONCE
            self.flag.overflow = int(self.flag.carry != high)

    elif (self.instruction == 'RCL'):
        src = self.fetch_operand(self.operands[0])
        count = self.fetch_operand(self.operands[1])
        c = count

        while (count):
            temp = self.flag.carry
            self.flag.carry = (src >> ((self.operand_size * 8) - 1)) & 1
            src = ((src << 1) + temp) & int('1' * self.operand_size * 8, 2)
            count -= 1

        self.write_operand(self.operands[0], src)

        high = (src >> ((self.operand_size * 8) - 1)) & 1           # overflow set only if shifted ONCE
        if (c == 1):
            self.flag.overflow = int(self.flag.carry != high)

    elif (self.instruction == 'RCR'):
        src = self.fetch_operand(self.operands[0])
        count = self.fetch_operand(self.operands[1])

        if (count == 1):
            high = (src >> ((self.operand_size * 8) - 1)) & 1           # overflow set only if shifted ONCE
            self.flag.overflow = int(self.flag.carry != high)

        while (count):
            temp = self.flag.carry
            self.flag.carry = src & 1
            src = (src >> 1) + (temp << ((self.operand_size * 8) - 1))
            src = src & int('1' * self.operand_size * 8, 2)
            count -= 1

        self.write_operand(self.operands[0], src)


        