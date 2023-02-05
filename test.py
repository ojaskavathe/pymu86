import re

text = '''a = ? \'hii ; this is not ? a comment\' ins \'this is ; not either\' ; this is a 'comment' ; this too
b = \'hello ; and this is not ? either\', ? ; this is a comment on the second line
   
;the line above is empty
c = \'hello ; and neither is this\' ; this is a comment on the third line'''

print(text)

# text = re.sub(r'(?m) *;.*n?', '', str(text))
# text = re.sub(
#     # r'^([^\';]*(\'[^\']*\')*)[ \t]*;.*$gm'
#     # r'^((?:[^\';]*(?:\'[^\']*\')?)*)[ \t]*;.*$g'
#     # r'^((?:[^\';]*(?:\'[^\']*\')?)*)[ \t]*;.*$/gm'
#     # r'^((?:[^\'";]*(?:\'[^\']*\'|"[^"]*")?)*)[ \t]*;.*$/gm'
#     # r'([^\';])*(\'[^\']*\')*'
#     , '', str(text), 0, re.MULTILINE)

# text = re.search(
#     r'^(?P<instruction>([^\';]*(\'[^\']*\'))*)[ \t]*(?P<comment>;.*)$'
#     , str(text), re.MULTILINE)
# print()
# print('instruction: ', text.group('instruction'))
# print('comment: ', text.group('comment'))

text = re.sub(
    r'^(?P<raw>([^\';]*(\'[^\']*\')[^\';]*)*)[ \t]*(?P<comment>;.*)$',
    r'\g<raw>',
    str(text), flags=re.MULTILINE)

# text = re.sub(
#     r"([^'\"]?)(\?)([^'\"])",
#     str(text), '0', flags=re.MULTILINE)

text = '\n'.join([line for line in text.split('\n') if line.strip() != ''])

# text = '''A ? with \"hello? what\" and single quoted \'?\'. It even has an escaped \\\'?\\\'!
# A foo with \"?\" and single quoted \'?\'. It even has an escaped \\\'?\\\' second line!'''

# print(text)  # after each change

# text = re.sub("(?<=[^\"'])({})(?=\\\\?[^\"'])".format('\?'),
#                     '0', text, flags=re.UNICODE)

# print()
# print(text)  # before the changes

def replace_callback(match):
    if match.group(2) is None:
        return match.group()
    return match.group(2).replace('?', '0')
text = re.sub('(\'[^\']*\'|"[^"]*")|(\?)', replace_callback, text)

print(text)

# print()

# text = re.sub("(?<=[^\"'])({})(?=\\\\?[^\"'])".format('\?'),
#                     '0', text, flags=re.UNICODE)

# print(text)  # after each change