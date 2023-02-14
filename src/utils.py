def to_dec(num):
    """Converts binary, octal, dec, hex strings to decimal base"""

    if isinstance(num, int):
        return num
    try:
        num = num.upper()
        if num.startswith('0X'):
            return int(num[2:], 16)
        elif num[-1] == 'H':
            return int(num.rstrip('H'), 16)
        elif num[-1] == 'D':
            return int(num.rstrip('D'), 10)
        elif num[-1] == 'O':
            return int(num.rstrip('O'), 8)
        elif num[-1] == 'B':
            return int(num.rstrip('B'), 2)
        else:
            return int(num)
    except:
        raise ValueError('\'num\' must be an integer.')