import re
import os

class Executable(object):
    def __init__(self, segments):
        self.name = ''
        self.title = ''
        self.segment_space = {}
        self.segment_names = {}
        self.segment_lengths = {}
        self.segment_addresses = {
            'CS': hex(segments['CS']),
            'DS': hex(segments['DS']),
            'SS': hex(segments['SS']),
            'ES': hex(segments['ES'])
        }
        self.instructions = []

def assemble(asm, segments):
    exec = Executable(segments)
    def _prep(asm):
        # Remove empty lines
        asm = (os.linesep).join([line for line in asm.splitlines() if line.strip() != ''])

        # Remove Comments
        # PS: I AM A LITERAL GOD
        # PPS: This took wayyyyy too long pls appreciate :/
        asm = re.sub(
            r'^(?P<raw>([^\'";]*((\'[^\']*\')|("[^"]*"))[^\'";]*)*)[ \t]*(?P<comment>;.*)$',
            r'\g<raw>',
            str(asm), flags=re.MULTILINE)
        
        # Replace ? with 0
        asm =  re.sub('(\'[^\']*\'|"[^"]*")|(\?)',
            lambda match: match.group() if match.group(2) is None else match.group(2).replace('?', '0'),
            asm)

        return asm
    asm = _prep(asm)
    print(asm)