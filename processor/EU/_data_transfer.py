from src import utils

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from processor.EU import EU

def data_transfer(self: "EU") -> None:
        if (self.instruction == 'MOV'):
            source = self.fetch_operand(self.operands[1])
            self.write_operand(self.operands[0], source)

        elif (self.instruction == 'PUSH'):
            source = self.fetch_operand(self.operands[0])
            self.increment_register('SP', -2)
            self.write_memory(self.effective_sp, source)

        elif (self.instruction == 'POP'):
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

        elif (self.instruction == 'XCHG'):
            a = self.fetch_operand(self.operands[0])
            b = self.fetch_operand(self.operands[1])
            self.write_operand(self.operands[0], b)
            self.write_operand(self.operands[1], a)

        elif (self.instruction == 'XLAT'):
            pass

        # I/O
        elif (self.instruction == 'IN'):
            # Input from port into AL or AX. IN AX, 4; IN AL, 7;
            # And we are not restricted to AL and AX, you can input to all regs.
            port = utils.decimal(self.operands[1])
            val = utils.decimal(input(f"Input to Port {port}: "))
            self.write_register(self.operands[0], val)

        elif (self.instruction == 'OUT'):
            # Output from AL or AX to port. OUT 4, AX; OUT DX, AX
            # And we are not restricted to AL and AX, you can output from all regs.
            # If port > 255, use DX.
            port = utils.decimal(self.operands[0])
            val = self.read_register(self.operands[1])
            self.print("> " * 16 + "@Port {}: 0x{:<4x} => {}\n".format(port, val, val))

        # Address-Object
        # elif (self.instruction == 'LEA'):
        #     # Parse all memory addressing modes: direct, register indirect, base, indexed, base indexed, relative base indexed
        #     # lea 0x3412:0x34; lea [si+bx]; lea 0x12; lea ss:offset; lea [bx][di]
        #     address_reg = ['BX', 'BP', 'SI', 'DI']
        #     segment_reg = ['CS', 'DS', 'SS', 'ES']
        #     opd = opd.split(':')[-1] # remove segment prefix
        #     par_list = utils.split_words(opd)
        #     offset = 0
        #     for par in par_list:
        #         if par in address_reg:
        #             offset += self.read_register(par)
        #         elif par in segment_reg:
        #             pass
        #         else:
        #             offset += utils.decimal(par)
        #     return offset