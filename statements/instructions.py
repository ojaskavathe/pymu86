data_transfer = [
    'MOV', 'PUSH', 'POP', 'XCHG', 'XLAT',                           # General Purpose
    'IN', 'OUT',                                                    # I/O
    'LEA', 'LDS', 'LES',                                            # Address Object
    'LAHF', 'SAHF', 'PUSHF', 'POPF'                                 # Flag Transfer
]

arithmetic = [
    'ADD', 'ADC', 'INC', 'AAA', 'DAA',                              # Addition
    'SUB', 'SBB', 'DEC', 'NEG', 'CMP', 'AAS', 'DAS',                # Subtraction
    'MUL', 'IMUL', 'AAM',                                           # Multiplication
    'DIV', 'IDIV', 'AAD', 'CBW', 'CWD'                              # Division
]

# Note that while SAL AND SHL are mnemonics for the same instruction,
# SAR and SHR are different instructions
bit_manipulation = [
    'NOT', 'AND', 'OR', 'XOR', 'TEST',                              # Logical
    'SAL', 'SHL', 'SAR', 'SHR',                                     # Shifts
    'ROL', 'ROR', 'RCL', 'RCR'                                      # Rotates
]

string = [
    'REP', 'REPE', 'REPZ', 'REPNE', 'REPNZ',                        # Repeat
    'MOVS', 'MOVSB', 'MOVSW',                                       # Move
    'CMPS', 'CMPSB', 'CMPSW',                                       # Compare
    'SCAS', 'SCASB', 'SCASW',                                       # Scan
    'LODS', 'LODSB', 'LODSW',                                       # Load
    'STOS', 'STOSB', 'STOSW'                                        # Store
]

core_transfer = [
    'JMP', 'CALL', 'RET', 'RETN', 'RETF',                           # Unconditional Transfers
    'LOOP', 'LOOPE', 'LOOPZ', 'LOOPNE', 'LOOPZE', 'JCXZ',           # Iteration Controls
    'INT', 'INTO', 'IRET'                                           # Interrupts
]

conditional_transfer = [
    'JA', 'JNBE', 'JAE', 'JNB', 'JB', 'JNAE', 'JBE', 'JNA',         # Conditional Transfers
    'JC', 'JZ', 'JE', 'JGE', 'JNL', 'JL', 'JNGE', 'JLE', 'JNG',
    'JNC', 'JNE', 'JNZ',
    'JNO', 'JNP', 'JPO', 'JNS', 'JO', 'JP', 'JPE', 'JS',
]

control_transfer = core_transfer + conditional_transfer

processor_control = [
    'STC', 'CLC', 'CMC', 'STD', 'CLD', 'STI', 'CLI',                # Flag Operations
    'HLT', 'WAIT', 'ESC', 'LOCK',                                   # External Synchronization
    'NOP'                                                           # No Operation
]

all = data_transfer + arithmetic + bit_manipulation + string + control_transfer + processor_control