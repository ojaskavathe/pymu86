data_transfer = [
    'MOV', 'PUSH', 'POP', 'XCHG', 'XLAT',                           # General Purpose
    'IN', 'OUT',                                                    # I/O
    'LEA', 'LDS', 'LES',                                            # Address Object
    'LAHS', 'SAHS', 'PUSHF', 'POPF'                                 # Flag Transfer
]

arithmetic = [
    'ADD', 'ADC', 'INC', 'AAA', 'DAA',                              # Addition
    'SUB', 'SBB', 'DEC', 'NEG', 'CMP', 'AAS', 'DAS',                # Subtraction
    'MUL', 'IMUL', 'AAM'                                            # Multiplication
    'DIV', 'IDIV', 'AAD', 'CBW', 'CWD'                              # Division
]

# Note that while SAL AND SHL are mnemonics for the same instruction,
# SAR and SHR are different instructions
bit_manipulation = [
    'NOT', 'AND', 'OR', 'XOR', 'TEST',                              # Logical
    'SHL', 'SAL', 'SHR', 'SAR',                                     # Shifts
    'ROL', 'ROR', 'RCL', 'RCR'                                      # Rotates
]

string = [
    'REP', 'REPE', 'REPZ', 'REPNE', 'REPNZ',                        # Repeat
    'MOVS', 'MOVSB', 'MOVSW',                                       # Move
    'CMPS',                                                         # Compare
    'SCAS', 'LODS', 'STOS'                                          # Scan, Load, Store
]

control_transfer = [
    'CALL', 'RET', 'JMP'                                            # Unconditional Transfers
    'JA', 'JNBE', 'JAE', 'JNB', 'JB', 'JNAE', 'JBE', 'JNA',         # Conditional Transfers
    'JC', 'JZ', 'JE', 'JGE', 'JNL', 'JL', 'JNGE', 'JLE', 'JNG',
    'JNC', 'JNE', 'JNZ',
    'JNO', 'JNP', 'JPO', 'JNS', 'JO', 'JP', 'JPE', 'JS',
    'LOOP', 'LOOPE', 'LOOPZ', 'LOOPNE', 'LOOPZE', 'JCXZ',           # Iteration Controls
    'INT', 'INTO', 'IRET'                                           # Interrupts
]

processor_control = [
    'STC', 'CLC', 'CMC', 'STD', 'CLD', 'STI', 'CLI',                # Flag Operations
    'HLT', 'WAIT', 'ESC', 'LOCK',                                   # External Synchronization
    'NOP'                                                           # No Operation
]