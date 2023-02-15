import re
import ast

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

def to_int(match):
    if(match.group('whole') is None):
        return match.group()
    else:
        before = match.group('integer')
        after = str(to_dec(before))
        return match.group('whole').replace(before, after)

def replaceNIQ(__str: str,__old: str, __new: str) -> str:
    def replace_callback(match):
        if match.group(2) is None:
            return match.group()
        return match.group(2).replace(__old, __new)
    return re.sub(r'(\'[^\']*\'|"[^"]*")|([' + __old + '])', replace_callback, __str)

string = '"a", 36h, \'50h, yo\''
# string = re.findall(r'(\'[^\']*\'|"[^"]*")|(?P<whole>(?P<integer>[0-9A-Fa-f]+[HhBbOo]{1})(?P<after>[,\s\]]+))', '[' + string + ']')
string = re.sub(r'(\'[^\']*\'|"[^"]*")|(?P<whole>(?P<integer>[0-9A-Fa-f]+[HhBbOo]{1})(?P<after>[,\s\]]+))',
    to_int,
    '[' + string + ']')
# string = re.sub(r"[0-9A-Fa-f]+[HhBbOo]{1}[,\s\]]+", to_int_str, '[' + string + ']')
# string = re.sub(r'([0-9A-Fa-f]+[HhBbOo]{1})([,\s\]]+)', to_int, '[' + string + ']')
lis = ast.literal_eval(string)

for i in lis:
    print(i)