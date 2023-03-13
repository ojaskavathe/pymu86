from src import utils
from statements import instructions

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from processor.EU import EU

def processor_control(self: "EU") -> None:

    # Flag Operations
    if (self.instruction == 'STC'):
        self.flag.carry = 1

    if (self.instruction == 'CLC'):
        self.flag.carry = 0

    if (self.instruction == 'CMC'):
        self.flag.carry ^= 1

    if (self.instruction == 'STD'):
        self.flag.direction = 1

    if (self.instruction == 'CLD'):
        self.flag.direction = 0

    if (self.instruction == 'STI'):
        self.flag.interrupt = 1

    if (self.instruction == 'CLI'):
        self.flag.interrupt = 0

    # External Synchronization
    if (self.instruction == 'HLT'):
        pass

    if (self.instruction == 'WAIT'):
        pass

    if (self.instruction == 'ESC'):
        pass

    if (self.instruction == 'LOCK'):
        pass

    # No Operation
    if (self.instruction == 'NOP'):
        pass

    