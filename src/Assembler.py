import re
import os
from src.statements import directives
from src import utils

class Executable(object):
    def __init__(self, segments):
        self.ip = 0                             # instruction pointer
        self.segment_space  = {}
        self.segment_addressability = {}        # label : segment
        self.segment_lengths = {}
        self.segment_addresses = {
            'CS': hex(segments['CS']),
            'DS': hex(segments['DS']),
            'SS': hex(segments['SS']),
            'ES': hex(segments['ES'])
        }
        self.labels = {}
        self.variables = {}
        self.statements = {}
        self.statements_raw = {}

def assemble(asm: str, segments: dict[str, int]) -> Executable:
    """Assemble the given assembly program into an \'executable\'."""

    exec = Executable(segments)
    
    exec.statements, exec.statements_raw = _prep(asm)
    exec.segment_addressability = _getSegmentAddressability(exec.statements)

    ip = 0
    while (ip < len(exec.statements)):
        currentStatement = exec.statements[ip]
        
        if(len(currentStatement) > 1 and currentStatement[1] == 'SEGMENT'):
            ip = _assembleSegment(ip, exec)
        
        ip += 1

    for i, line in enumerate(exec.statements):
        print(i, line, sep='\t')

    return exec

def _assembleSegment(ip: int, exec: Executable) -> int:
    """Initialize segment memory and assembly all statements in a segment."""

    relative_ip = 0
    segment_label = exec.statements[ip][0]                          # CODE, DATA
    segment = exec.segment_addressability[segment_label]            # which segment: CS, DS etc.
    exec.segment_space[segment] = [['0']] * int('10000', 16)          # empty segment

    for segment_ip in range(ip + 1, len(exec.statements)):
        currentStatement = exec.statements[segment_ip]
        currentStatement_raw = exec.statements_raw[segment_ip]
        for word_index in range(len(currentStatement)):
            if(currentStatement[word_index] == '$'):
                currentStatement[word_index] = relative_ip

        if(currentStatement[0] == segment_label):
            if(currentStatement[1] != 'ENDS'):
                raise SyntaxError(segment_label + ' Segment Doesn\'t End.')
            exec.segment_lengths[segment] = relative_ip
            return segment_ip
        elif(':' in currentStatement[0]):                           # handle labels
            label_line = currentStatement[0].split(':')
            exec.labels[label_line[0]] = {
                'segment_address':  exec.segment_addresses[segment],
                'offset':           hex(relative_ip)
            }
            if(len(currentStatement) == 1):                         # label:
                pass                                                #       mov ax, bx
            else:   
                if(label_line[1]):                                  # label:mov ax, bx
                    currentStatement[0] = label_line[1] 
                else:                                               # label: mov ax, bx
                    currentStatement = currentStatement[1:]
                exec.segment_space[segment][segment_ip] = currentStatement
                relative_ip += 1
        elif(currentStatement[0] in directives.data_definition):    # DB 15, 47, 'hello'
            varBytes = _toBytes(currentStatement, currentStatement_raw)
            exec.segment_space[segment][segment_ip:segment_ip + len(varBytes)] = varBytes
            relative_ip += len(varBytes)
        elif(len(currentStatement) > 2 and currentStatement[1] in directives.data_definition):
            exec.variables[currentStatement[0]] = {
                'segment_address':  exec.segment_addresses[segment],
                'offset':           hex(relative_ip)
            }
            # remove name of var from statement:
            # varName db values => db values 
            withoutName = currentStatement_raw.replace(currentStatement_raw.split()[0], '', 1).strip()
            varBytes = _toBytes(currentStatement[1:], withoutName)
            exec.segment_space[segment][segment_ip:segment_ip + len(varBytes)] = varBytes
            relative_ip += len(varBytes)
        else:                                                       # add instruction to current segment's space
            exec.segment_space[segment][segment_ip] = currentStatement
            relative_ip += 1
    
    raise SyntaxError(segment_label + ' Segment doesn\'t end.')


def _toBytes(dir: list[str], dir_raw: str) -> list[str]:
    """Return the data defined in the given directive as a list of bytes."""

    varType = dir[0]
    varType_raw = dir_raw.split()[0]
    varBytes = []
    
    # DB repeatVal DUP (val1, val2) | DB repeatVal DUP(val)
    if(len(dir) > 2 and dir[2][:3] == 'DUP'):
        repeatVal = utils.to_dec(dir[1])
        vals = dir_raw[dir_raw.find('(') + 1 : -1]
        repeat_raw = varType + ' ' + vals                                               # DB val1, val2
        repeat = [s for s in re.split(r'[ |,]', repeat_raw.strip().upper()) if s]       # ['DB', 'VAL1', 'VAL2']
        return _toBytes(repeat, repeat_raw) * repeatVal

def _getSegmentAddressability(statements: list[list[str]]) -> dict[str, str]:
    """Get the addressability of a segment. Returns a dict in the format { CS : code, DS : data }"""

    addressability = {}
    for statement in statements:
        if statement[0] == 'ASSUME':
            for seg in statement[1:]:
                seg = seg.split(':')
                addressability[seg[1]] = seg[0]     # data is addressable through ds etc.
            break
    return addressability                           # label : segment

def _prep(asm: str) -> tuple[list[list[str]], list[str]]:
    """Remove Comments, Empty Lines, and some cleanup to prepare for assembly."""

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

    # list of statements (split) (uppercase)
    statements = []
    raw_statements = []
    for line in asm.split(os.linesep):
        statements.append([word for word in re.split(" |,", line.strip().upper()) if word])
        raw_statements.append(line.strip())

    return statements, raw_statements