import re
import os

class Executable(object):
    def __init__(self, segments):
        self.ip = 0                             # instruction pointer
        self.segment_space = {}
        self.segment_addressability = {}        # label : segment
        self.segment_lengths = {}
        self.segment_addresses = {
            'CS': hex(segments['CS']),
            'DS': hex(segments['DS']),
            'SS': hex(segments['SS']),
            'ES': hex(segments['ES'])
        }
        self.statements = []
        self.statements_raw = []

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
    exec.segment_space[segment] = [['0']] * int('100', 16)          # empty segment

    for segment_ip in range(ip + 1, len(exec.statements)):
        currentStatement = exec.statements[segment_ip]
        
        for word_index in range(len(currentStatement)):
            if(currentStatement[word_index] == '$'):
                currentStatement[word_index] = relative_ip

        if(currentStatement[0] == segment_label):
            assert currentStatement[1] == 'ENDS', 'Segment Doesn\'t End'
            exec.segment_lengths[segment] = relative_ip
            return segment_ip
        else:
            relative_ip += 1

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