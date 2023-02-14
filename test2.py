import re

def to_dec(num):
    """Converts binary, octal, dec, hex strings to decimal base"""

    if isinstance(num, int):
        return num
    num = num.upper()
    if num.startswith('0X'):
        return int(num[2:], 16)
    if num[-1] == 'B':
        res = int(num.rstrip('B'), 2)
    elif num[-1] == 'O':
        res = int(num.rstrip('O'), 8)
    elif num[-1] == 'D':
        res = int(num.rstrip('D'), 10)
    elif num[-1] == 'H':
        res = int(num.rstrip('H'), 16)
    else:
        res = int(num)
    return res

def to_int_str(matched):
    string = matched.group()
    idx = re.search(r'[,\s\]]', string).span()[0]
    suffix = string[idx:]
    string = string[:idx]
    int_str = str(to_dec(string))
    # print("int_st:", int_str)
    return int_str + suffix

string = '\'a\', "30h yo"'
string = re.sub(r"[0-9A-Fa-f]+[HhBbOo]{1}[,\s\]]+", to_int_str, '[' + string + ']')

a = ''
s = re.search(r'[,\s\]]', a)

print(s)