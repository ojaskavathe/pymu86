import re

# text = 'a = \'hii ; this is not a comment\' ins \'this is ; not either\' ; this is a comment ; this too'
# text = 'a = \'hello ; this isn\'t a comment either\' ; this is a comment on the second line'
text = '''a = \'hii ; this is not a comment\' ins \'this is ; not either\' ; this is a comment ; this too
a = \'hello ; this is not a comment either\' ; this is a comment on the second line
b = \'hello ; and neither is this \' ; this is a comment on the third line'''

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
    r'^(?P<raw>([^\';]*(\'[^\']*\'))*)[ \t]*(?P<comment>;.*)$',
    r'\g<raw>',
    str(text), flags=re.MULTILINE)
print()
print(text)