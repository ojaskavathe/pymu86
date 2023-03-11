from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from processor.EU import EU

def arithmetic(self: "EU") -> None:
    if (self.instruction == 'ADD'):
        a = self.fetch_operand(self.operands[0])
        b = self.fetch_operand(self.operands[1])
        res = (a + b) & int('0x' + 'f' * self.operand_size * 2, 16)