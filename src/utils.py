import re
import ast

def decimal(num: int) -> str:
    """Convert binary, octal, dec, hex strings to decimal base 10"""

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

def replaceNIQ(__str: str,__old: str, __new: str) -> str:
    """Return a copy of string str with occurences of substring old (EXCEPT those within quoted substrings) replaced by substring new."""

    def replace_callback(match):
        a = match.group(2)
        if match.group(2) is None:
            return match.group()
        return match.group(2).replace(__old, __new)

    old_esc = re.escape(__old)
    return re.sub(fr'(\'[^\']*\'|"[^"]*")|({old_esc})', replace_callback, __str)

def splitNIQ(__str: str) -> list[str]:
    """Return a list of the substrings in str separated by space. Doesn't split within quoted substrings. CURRENTLY BROKEN"""

    return [p for p in re.split(r'([ ]|\'[^\']*\'|"[^"]*")', __str) if p.strip()]

def dataList(string: str) -> list:
    """Return a list of values retrieved from the data definition directive. Also converts hex, oct, binary integers to decimal."""

    def _int_string(match):
        if(match.group('whole') is None):
            return match.group()
        else:
            before = match.group('integer')
            after = str(decimal(before))
            return match.group('whole').replace(before, after)

    out = re.sub(r'(\'[^\']*\'|"[^"]*")|(?P<whole>(?P<integer>[0-9A-Fa-f]+[HhBbOo]{1})(?P<after>[,\s\]]+))',
        _int_string,
        '[' + string + ']')
    return ast.literal_eval(out)
