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
        self.instructions_raw = []

def assemble(asm, segments):
    exec = Executable(segments)
    
    exec.instructions, exec.instructions_raw = _prep(asm)
    print(exec.instructions_raw)

def _prep(asm):
    # Remove Comments
    asm = asm + ';'     # Regex breaks if file doesn't end with ';'
    asm = re.sub(
    r'^((?:[^\'";]*(?:\'[^\']*\'|"[^"]*")?)*)[ \t]*;.*$',
    r'\1',
    str(asm), flags=re.MULTILINE)

    # Remove empty lines
    asm = (os.linesep).join([line for line in asm.splitlines() if line.strip() != ''])
    
    # Replace ? with 0
    asm =  re.sub('(\'[^\']*\'|"[^"]*")|(\?)',
        lambda match: match.group() if match.group(2) is None else match.group(2).replace('?', '0'),
        asm)

    #list of instructions
    instructions = []
    raw_instructions = []
    for line in asm.split(os.linesep):
        instructions.append([word for word in re.split(" |,", line.strip().upper()) if word])
        raw_instructions.append(line.strip())

    return instructions, raw_instructions