import re

text = '''a = ? \'hii ; this is not ? a comment\' ins \'this is ; not either\' ; this is a 'comment' ; this too
b = \'hello ; and this is not ? either\', ? ; this is a comment on the second line
lol ;normal   
;the line above is empty
c = \"hello ; and neither is this\" ; this is a "comment" on the third line'''

text = '''ASSUME CS:CODE,DS:DATA

DATA SEGMENT ;asd
    msg db "h;ello$", ? ; this is a comme'nt ; sdf'sd 
DATA ENDS

CODE SEGMENT
   start: 
        mov ax, 1000h
        mov bl, 0
        div bl
        mov ah,4ch
        int 21h  

CODE ENDS
END START
        cmp   byte [si], 0x2B ;
'''

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
text = '\n'.join([line for line in text.split('\n') if line.strip() != ''])

text = re.sub(
    r'^((?:[^\'";]*(?:\'[^\']*\'|"[^"]*")?)*)[ \t]*;.*$',
    r'\1',
    str(text), flags=re.MULTILINE)

# text = re.findall(
#     r'^((?:[^";]*(?:"[^"]*"))*)(.*)$',
#     str(text), flags=re.MULTILINE)

print(text)

# text = re.sub(
#     r"([^'\"]?)(\?)([^'\"])",
#     str(text), '0', flags=re.MULTILINE)


# text = '''A ? with \"hello? what\" and single quoted \'?\'. It even has an escaped \\\'?\\\'!
# A foo with \"?\" and single quoted \'?\'. It even has an escaped \\\'?\\\' second line!'''

# print(text)  # after each change

# text = re.sub("(?<=[^\"'])({})(?=\\\\?[^\"'])".format('\?'),
#                     '0', text, flags=re.UNICODE)

# print()
# print(text)  # before the changes

#### def replace_callback(match):
####     if match.group(2) is None:
####         return match.group()
####     return match.group(2).replace('?', '0')
#### text = re.sub('(\'[^\']*\'|"[^"]*")|(\?)', replace_callback, text)

# print()
# print(text)

# print()

# text = re.sub("(?<=[^\"'])({})(?=\\\\?[^\"'])".format('\?'),
#                     '0', text, flags=re.UNICODE)

# print(text)  # after each change