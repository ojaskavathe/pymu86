from src import utils

class FlagRegister:

    def __init__(self) -> None:
        self.overflow: int = 0
        self.direction: int = 0
        self.interrupt: int = 0
        self.trap: int = 0
        self.sign: int = 0
        self.zero: int = 0
        self.auxiliary: int = 0
        self.parity: int = 0
        self.carry: int = 0

    def get(self) -> int:
        return (self.overflow << 11) + \
               (self.direction << 10) + \
               (self.interrupt << 9) + \
               (self.trap << 8) + \
               (self.sign << 7) + \
               (self.zero << 6) + \
               (self.auxiliary << 4) + \
               (self.parity << 2) + \
               (self.carry)
    
    def set_parity(
        self,
        res: int
    ) -> None:
        # count no. of 1 in res (binary)
        ones = 0
        while res > 0:
            ones += 1
            res &= res - 1
        
        if (ones % 2 == 0):
            self.parity = 1
        else:
            self.parity = 0

    def set_overflow(
        self,
        res: int,
        bytes: int
    ) -> None:
    
        # Checking whether {res} overflows according to the range of signed numbers that {bytes} can store
        min = utils.signed(int('1' + (bytes * 8 - 1) * '0', 2), bytes)      # 1000 0000 for 1 byte
        max = utils.signed(int('0' + (bytes * 8 - 1) * '1', 2), bytes)      # 0111 1111 for 1 byte
        has_overflowed = (res > max or res < min)

        if (has_overflowed):
            self.overflow = 1
        else:
            self.overflow = 0
    
    def set_sign(
        self,
        res: int,
        bytes: int
    ) -> None:
        if(utils.signed(res, bytes) < 0):
            self.sign = 1
        else:
            self.sign = 0

    def set_zero(
        self,
        res: int
    ) -> None:
        if(res == 0):
            self.zero = 1
        else:
            self.zero = 0

    def set_carry(
        self,
        res: bool
    ) -> None:
        if(res == True):
            self.carry = 1
        else:
            self.carry = 0