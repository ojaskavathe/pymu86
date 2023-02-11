import re
import os

class Executable(object):
    def __init__(self, segments):
        self.segment_space = {}
        self.segment_addressability = {}
        self.segment_lengths = {}
        self.segment_addresses = {
            'CS': hex(segments['CS']),
            'DS': hex(segments['DS']),
            'SS': hex(segments['SS']),
            'ES': hex(segments['ES'])
        }
        self.statements = []
        self.statements_raw = []

def assemble(asm, segments):
    exec = Executable(segments)
    
    exec.statements, exec.statements_raw = _prep(asm)
    exec.segment_addressability = _getSegmentAddressability(exec.statements)
    # for i in exec.statements:
    #     print(i)
    for ip in range(len(exec.statements)):
        print(ip, exec.statements[ip])

    # print(exec.segment_addressability)  

def _getSegmentAddressability(statements):
    addressability = {}
    for statement in statements:
        if statement[0] == 'ASSUME':
            for seg in statement[1:]:
                seg = seg.split(':')
                addressability[seg[1]] = seg[0]     # data is addressable through ds etc.
            break
    return addressability

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

    # list of instructions
    statements = []
    raw_statements = []
    for line in asm.split(os.linesep):
        statements.append([word for word in re.split(" |,", line.strip().upper()) if word])
        raw_statements.append(line.strip())

    return statements, raw_statements