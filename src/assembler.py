import re
import os
from src.executable import Executable
from statements import instructions, directives
from src import utils

def assemble(
    asm: str, 
    segments: dict[str, int]
) -> Executable:
    """Assemble the given assembly program into an \'executable\'."""

    exec = Executable(segments)
    
    exec.statements, exec.statements_raw = _prep(asm)
    exec.segment_addressability = _getSegmentAddressability(exec.statements)

    ip = 0
    while (ip < len(exec.statements)):
        currentStatement = exec.statements[ip]
        if(len(currentStatement) > 1 and currentStatement[1] == 'SEGMENT'):
            ip = _assembleSegment(ip, exec)
        elif(currentStatement[0] == 'END' and currentStatement[1] in exec.labels):
            exec.ip = exec.labels[currentStatement[1]]['offset']            # END START
        
        ip += 1

    _evaluate_labels(exec)

    for i, line in enumerate(exec.statements):
        print(i, line, sep='\t')

    return exec

def _evaluate_labels(
    exec: Executable
) -> None:
    """Change all labels (variables, segments, jump labels) to memory addresses in the instructions."""
    labels = {}

    # segment labels ('DATA': 'DS' etc)
    for seg_label, seg in exec.segment_addressability.items():
        labels[seg_label] = str(exec.segment_address[seg])
    
    # variables
    for var_label, var_details in exec.variables.items():
        for seg, address in exec.segment_address.items():
            if (var_details['segment_address'] == address):
                segment_name = seg
        labels[var_label] = segment_name + ':[' + var_details['offset'] + ']'

    # changing labels to addresses in memory
    for segment, data in exec.segment_space.items():
        segment_length = exec.segment_lengths[segment]
        for index in range(segment_length):
            current_ins = data[index]
            if (current_ins[0] in instructions.transfer_control and current_ins[-1] in exec.labels):
                pass
            for i, word in enumerate(current_ins):
                for label, value in labels.items():
                    if (word == label):
                        exec.segment_space[segment][index][i] = value
                    
                

def _assembleSegment(
    ip: int, 
    exec: Executable
) -> int:
    """Initialize segment memory and assembly all statements in a segment."""

    relative_ip = 0
    segment_label = exec.statements[ip][0]                          # CODE, DATA etc
    segment = exec.segment_addressability[segment_label]            # CS, DS etc.
    exec.segment_space[segment] = [['0']] * int('10000', 16)        # fill segment with empty lists instead of just zeroes

    for segment_ip in range(ip + 1, len(exec.statements)):
        currentStatement = exec.statements[segment_ip]
        currentStatement_raw = exec.statements_raw[segment_ip]
        for word_index in range(len(currentStatement)):             # replace $ with segment ip
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
                'segment_address':  exec.segment_address[segment],
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
            varBytes = _bytes(currentStatement, currentStatement_raw)
            exec.segment_space[segment][segment_ip:segment_ip + len(varBytes)] = varBytes
            relative_ip += len(varBytes)

        elif(len(currentStatement) > 2 and currentStatement[1] in directives.data_definition):
            exec.variables[currentStatement[0]] = {
                'segment_address':  exec.segment_address[segment],
                'offset':           hex(relative_ip)
            }
            # remove name of var from statement:
            # varName db values -> db values 
            withoutName = currentStatement_raw.replace(currentStatement_raw.split()[0], '', 1).strip()
            varBytes = _bytes(currentStatement[1:], withoutName)
            exec.segment_space[segment][relative_ip:relative_ip + len(varBytes)] = varBytes
            relative_ip += len(varBytes)

        else:                                                       # add instruction to current segment's space
            exec.segment_space[segment][relative_ip] = currentStatement
            relative_ip += 1
    
    raise SyntaxError(segment_label + ' Segment doesn\'t end.')


def _bytes(
    dir: list[str], 
    dir_raw: str
) -> list[str]:
    """Return the data defined in the given directive as a list of bytes."""

    varType = dir[0]
    varType_raw = dir_raw.split()[0]
    varBytes = []
    
    # DB repeatVal DUP (val1, val2) | DB repeatVal DUP(val)
    if(len(dir) > 2 and dir[2][:3] == 'DUP'):
        repeatVal = utils.decimal(dir[1])
        vals = dir_raw[dir_raw.find('(') + 1 : -1]                                      # val1, 'val2', 30h
        repeat_raw = varType + ' ' + vals                                               # DB val1, 'val2', 30h
        repeat = [s for s in re.split(r'[ |,]', repeat_raw.strip().upper()) if s]       # ['DB', 'VAL1', '\'VAL2\'', '30h']
        return _bytes(repeat, repeat_raw) * repeatVal

    elif(varType == 'DB'):
        vals_raw = utils.replaceNIQ(dir_raw, varType_raw, '').strip()                   # val1, 'val2', 30h
        data_list = utils.dataList(vals_raw)                                            # [val1, 'val2', 48]
        byte_list = []
        for val in data_list:
            if(isinstance(val, int)):
                byte_list.append([hex(val)])
            elif(isinstance(val, str)):
                for char in val:
                    byte_list.append([hex(ord(char))])
        return byte_list

    elif(varType == 'DW'):
        pass
    
    elif(varType == 'DD'):
        pass

def _getSegmentAddressability(
    statements: list[list[str]]
) -> dict[str, str]:
    """Get the addressability of a segment. Returns a dict in the format { CS : code, DS : data }"""

    addressability = {}
    for statement in statements:
        if statement[0] == 'ASSUME':
            for seg in statement[1:]:
                seg = seg.split(':')
                addressability[seg[1]] = seg[0]     # data is addressable through ds etc.
            break
    return addressability                           # label : segment

def _prep(
    asm: str
) -> tuple[list[list[str]], list[str]]:
    """Remove Comments, Empty Lines, and some cleanup to prepare for assembly."""

    # Remove Comments
    asm = asm + ';'                                 # Regex breaks if file doesn't end with ';'
    asm = re.sub(
        r'^((?:[^\'";]*(?:\'[^\']*\'|"[^"]*")?)*)[ \t]*;.*$',
        r'\1',
        str(asm), flags=re.MULTILINE)

    # Remove empty lines
    asm = (os.linesep).join([line for line in asm.splitlines() if line.strip() != ''])
    
    # Replace ? with 0
    asm = utils.replaceNIQ(asm, '?', '0')

    # list of statements (split) (uppercase)
    statements = []
    raw_statements = []
    for line in asm.split(os.linesep):
        statements.append([word for word in re.split(" |,", line.strip().upper()) if word])
        # statements.append(utils.splitNIQ(line.strip().upper()))
        raw_statements.append(line.strip())

    return statements, raw_statements
