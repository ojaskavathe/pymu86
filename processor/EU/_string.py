from src import utils

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from processor.EU import EU

def string(self: "EU") -> None:

    # Repeat
    if (self.instruction == 'REP'):
        self.instruction = self.operands[0]
        self.operands = self.operands[1:]
        self.fetch_operand_size()

        while (self.read_register('CX') != 0):
            self.execute()
            c = self.read_register('CX')
            self.write_register('CX', c - 1)

    elif (self.instruction == 'REPE' or \
        self.instruction == 'REPZ'):

        self.instruction = self.operands[0]
        self.operands = self.operands[1:]
        self.fetch_operand_size()

        while (self.read_register('CX') != 0):
            self.execute()
            c = self.read_register('CX')
            self.write_register('CX', c - 1)
            if (self.flag.zero == 0):
                break

    elif (self.instruction == 'REPNE' or \
        self.instruction == 'REPNZ'):
        
        self.instruction = self.operands[0]
        self.operands = self.operands[1:]
        self.fetch_operand_size()

        while (self.read_register('CX') != 0):
            self.execute()
            c = self.read_register('CX')
            self.write_register('CX', c - 1)
            if (self.flag.zero == 1):
                break

    # Move
    elif (self.instruction == 'MOVS'):
        src  = (self.bus.registers['DS'] * 16) + self.gpr['SI']
        dest = (self.bus.registers['ES'] * 16) + self.gpr['DI']

        if (self.operand_size == 1):
            data_list = self.bus.read_byte(src)
        else:
            data_list = self.bus.read_word(src)

        out = 0
        for res in data_list:
            out = (out << 8) + (int(res, 16) & 0xff)
        self.write_memory(dest, out)

        if(self.flag.direction == 0):
            self.increment_register('SI', self.operand_size)
            self.increment_register('DI', self.operand_size)
        else:
            self.increment_register('SI', -self.operand_size)
            self.increment_register('DI', -self.operand_size)

    elif (self.instruction == 'MOVSB'):
        self.operand_size = 1
        src  = (self.bus.registers['DS'] * 16) + self.gpr['SI']
        dest = (self.bus.registers['ES'] * 16) + self.gpr['DI']
        data_list = self.bus.read_byte(src)
        out = 0
        for res in data_list:
            out = (out << 8) + (int(res, 16) & 0xff)

        self.write_memory(dest, out)

        if(self.flag.direction == 0):
            self.increment_register('SI', 1)
            self.increment_register('DI', 1)
        else:
            self.increment_register('SI', -1)
            self.increment_register('DI', -1)

    elif (self.instruction == 'MOVSW'):
        self.operand_size = 2
        src  = (self.bus.registers['DS'] * 16) + self.gpr['SI']
        dest = (self.bus.registers['ES'] * 16) + self.gpr['DI']
        data_list = self.bus.read_word(src)
        out = 0
        for res in data_list:
            out = (out << 8) + (int(res, 16) & 0xff)

        if(self.flag.direction == 0):
            self.increment_register('SI', 2)
            self.increment_register('DI', 2)
        else:
            self.increment_register('SI', -2)
            self.increment_register('DI', -2)

    # Compare
    elif (self.instruction == 'CMPS'):
        src  = (self.bus.registers['DS'] * 16) + self.gpr['SI']
        dest = (self.bus.registers['ES'] * 16) + self.gpr['DI']

        if (self.operand_size == 1):
            src_list  = self.bus.read_byte(src)
            dest_list = self.bus.read_byte(dest)
        else:
            src_list  = self.bus.read_word(src)
            dest_list = self.bus.read_word(dest)

        a = 0
        for res in src_list:
            a = (a << 8) + (int(res, 16) & 0xff)

        b = 0
        for res in dest_list:
            b = (b << 8) + (int(res, 16) & 0xff)

        res = (a - b) & int('1' * self.operand_size * 8, 2)
        self.flag.set_overflow(a - b, self.operand_size)
        self.flag.set_carry(utils.unsigned(a, self.operand_size) < utils.unsigned(b, self.operand_size))
        self.flag.set_parity(res)
        self.flag.set_zero(res)
        self.flag.set_sign(res, self.operand_size)

        if(self.flag.direction == 0):
            self.increment_register('SI', self.operand_size)
            self.increment_register('DI', self.operand_size)
        else:
            self.increment_register('SI', -self.operand_size)
            self.increment_register('DI', -self.operand_size)

    elif (self.instruction == 'CMPSB'):
        self.operand_size = 1
        src  = (self.bus.registers['DS'] * 16) + self.gpr['SI']
        dest = (self.bus.registers['ES'] * 16) + self.gpr['DI']
        
        src_list  = self.bus.read_byte(src)
        dest_list = self.bus.read_byte(dest)
        
        a = 0
        for res in src_list:
            a = (a << 8) + (int(res, 16) & 0xff)

        b = 0
        for res in dest_list:
            b = (b << 8) + (int(res, 16) & 0xff)

        res = (a - b) & int('1' * self.operand_size * 8, 2)
        self.flag.set_overflow(a - b, self.operand_size)
        self.flag.set_carry(utils.unsigned(a, self.operand_size) < utils.unsigned(b, self.operand_size))
        self.flag.set_parity(res)
        self.flag.set_zero(res)
        self.flag.set_sign(res, self.operand_size)

        if(self.flag.direction == 0):
            self.increment_register('SI', 1)
            self.increment_register('DI', 1)
        else:
            self.increment_register('SI', -1)
            self.increment_register('DI', -1)

    elif (self.instruction == 'CMPSW'):
        self.operand_size = 2
        src  = (self.bus.registers['DS'] * 16) + self.gpr['SI']
        dest = (self.bus.registers['ES'] * 16) + self.gpr['DI']
        src_list  = self.bus.read_word(src)
        dest_list = self.bus.read_word(dest)
        
        a = 0
        for res in src_list:
            a = (a << 8) + (int(res, 16) & 0xff)

        b = 0
        for res in dest_list:
            b = (b << 8) + (int(res, 16) & 0xff)

        res = (a - b) & int('1' * self.operand_size * 8, 2)
        self.flag.set_overflow(a - b, self.operand_size)
        self.flag.set_carry(utils.unsigned(a, self.operand_size) < utils.unsigned(b, self.operand_size))
        self.flag.set_parity(res)
        self.flag.set_zero(res)
        self.flag.set_sign(res, self.operand_size)

        if(self.flag.direction == 0):
            self.increment_register('SI', 2)
            self.increment_register('DI', 2)
        else:
            self.increment_register('SI', -2)
            self.increment_register('DI', -2)

    # Scan
    elif (self.instruction == 'SCAS'):
        dest = (self.bus.registers['ES'] * 16) + self.gpr['DI']
        if (self.operand_size == 1):
            dest_list = self.bus.read_byte(dest)
            a = self.read_register('AL')
        else:
            dest_list = self.bus.read_word(dest)
            a = self.read_register('AX')                

        b = 0
        for res in dest_list:
            b = (b << 8) + (int(res, 16) & 0xff)

        res = (a - b) & int('1' * self.operand_size * 8, 2)
        self.flag.set_overflow(a - b, self.operand_size)
        self.flag.set_carry(utils.unsigned(a, self.operand_size) < utils.unsigned(b, self.operand_size))
        self.flag.set_parity(res)
        self.flag.set_zero(res)
        self.flag.set_sign(res, self.operand_size)

        if(self.flag.direction == 0):
            self.increment_register('DI', self.operand_size)
        else:
            self.increment_register('DI', -self.operand_size)

    elif (self.instruction == 'SCASB'):
        self.operand_size = 1
        dest = (self.bus.registers['ES'] * 16) + self.gpr['DI']
        dest_list = self.bus.read_byte(dest)
        
        a = self.read_register('AL')

        b = 0
        for res in dest_list:
            b = (b << 8) + (int(res, 16) & 0xff)

        res = (a - b) & int('1' * self.operand_size * 8, 2)
        self.flag.set_overflow(a - b, self.operand_size)
        self.flag.set_carry(utils.unsigned(a, self.operand_size) < utils.unsigned(b, self.operand_size))
        self.flag.set_parity(res)
        self.flag.set_zero(res)
        self.flag.set_sign(res, self.operand_size)

        if(self.flag.direction == 0):
            self.increment_register('DI', 1)
        else:
            self.increment_register('DI', -1)

    elif (self.instruction == 'SCASW'):
        self.operand_size = 2
        dest = (self.bus.registers['ES'] * 16) + self.gpr['DI']
        dest_list = self.bus.read_word(dest)
        
        a = self.read_register('AX')

        b = 0
        for res in dest_list:
            b = (b << 8) + (int(res, 16) & 0xff)

        res = (a - b) & int('1' * self.operand_size * 8, 2)
        self.flag.set_overflow(a - b, self.operand_size)
        self.flag.set_carry(utils.unsigned(a, self.operand_size) < utils.unsigned(b, self.operand_size))
        self.flag.set_parity(res)
        self.flag.set_zero(res)
        self.flag.set_sign(res, self.operand_size)

        if(self.flag.direction == 0):
            self.increment_register('DI', 2)
        else:
            self.increment_register('DI', -2)

    # Load
    elif (self.instruction == 'LODS'):
        src_adr = (self.bus.registers['ES'] * 16) + self.gpr['DI']
        if (self.operand_size == 1):
            src_list = self.bus.read_byte(src_adr)
            dest = 'AL'
        else:
            src_list = self.bus.read_word(src_adr)
            dest = 'AX'

        src = 0
        for res in src_list:
            src = (src << 8) + (int(res, 16) & 0xff)

        self.write_register(dest, src)

        if(self.flag.direction == 0):
            self.increment_register('DI', self.operand_size)
        else:
            self.increment_register('DI', -self.operand_size)

    elif (self.instruction == 'LODSB'):
        src_adr = (self.bus.registers['ES'] * 16) + self.gpr['DI']
        src_list = self.bus.read_byte(src_adr)        

        src = 0
        for res in src_list:
            src = (src << 8) + (int(res, 16) & 0xff)

        self.write_register('AL', src)

        if(self.flag.direction == 0):
            self.increment_register('DI', 1)
        else:
            self.increment_register('DI', -1)

    elif (self.instruction == 'LODSW'):
        src_adr = (self.bus.registers['ES'] * 16) + self.gpr['DI']
        src_list = self.bus.read_word(src_adr)        

        src = 0
        for res in src_list:
            src = (src << 8) + (int(res, 16) & 0xff)

        self.write_register('AX', src)

        if(self.flag.direction == 0):
            self.increment_register('DI', 2)
        else:
            self.increment_register('DI', -2)

    # Store
    elif (self.instruction == 'STOS'):
        dest = (self.bus.registers['ES'] * 16) + self.gpr['DI']
        if (self.operand_size == 1):
            src = self.read_register('AL')
        else:
            src = self.read_register('AX')

        self.write_memory(dest, src)

        if(self.flag.direction == 0):
            self.increment_register('DI', self.operand_size)
        else:
            self.increment_register('DI', -self.operand_size)

    elif (self.instruction == 'STOSB'):
        dest = (self.bus.registers['ES'] * 16) + self.gpr['DI']
        src = self.read_register('AL')

        self.write_memory(dest, src)

        if(self.flag.direction == 0):
            self.increment_register('DI', 1)
        else:
            self.increment_register('DI', -1)

    elif (self.instruction == 'STOSW'):
        dest = (self.bus.registers['ES'] * 16) + self.gpr['DI']
        src = self.read_register('AL')

        self.write_memory(dest, src)

        if(self.flag.direction == 0):
            self.increment_register('DI', 2)
        else:
            self.increment_register('DI', -2)
