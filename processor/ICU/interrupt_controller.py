from src.executable import Executable
from src.assembler import assemble

SEG_INIT = {
    'DS': int('0000', 16),  # Initial value of data segment
    'CS': int('1000', 16),  # Initial value of code segment
    'SS': int('0000', 16),  # Initial value of stack segment
    'ES': int('0000', 16)   # Initial value of extra segment
}

def load_ivt(
    memory
): # Interrupt Vector Table
    # 0000:0000 ~ 0000:03FF 
    for i in range(256):                                                # 0 - 3FF
        memory.write_byte(i * 4, '0x00')                                      # IP
        memory.write_byte(i * 4 + 1, '0x00')
        memory.write_byte(i * 4 + 2, str(hex(i % 16)) + '0')                  # CS
        memory.write_byte(i * 4 + 3, '0x1' + str(hex(i // 16))[-1])

def load_isr(
    memory,
    debug: bool
) -> None:
    load_ivt(memory)
    if (debug):
        print("loading ISR...")

    for i in ['0', '1', '2', '3', '4', '7c']:
        with open("./processor/ICU/ISRs/isr" + i + ".asm", 'r', encoding='utf-8') as file:
            asm_code = file.read()
            
        isr = assemble(asm_code, SEG_INIT)

        length = isr.segment_lengths['CS']
        base = (int('1000', 16) << 4) + int('100', 16) * int('0x'+i, 16)
        memory.space[base : base + length] = isr.segment_space['CS'][:length]