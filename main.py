from src.executable import Executable
from src.assembler import assemble
from processor.memory import Memory
from processor.cpu import CPU

MEMORY_SIZE = int('FFFFF', 16)  # 1  MB
SEGMENT_SIZE = int('10000', 16) # 64 KB
DEBUG = False

# initial offsets
SEGMENTS = {
    'CS': int('2000', 16),
    'DS': int('3000', 16),
    'SS': int('5000', 16),
    'ES': int('7000', 16),
}

if __name__ == "__main__":
    memory = Memory(SEGMENT_SIZE, MEMORY_SIZE)

    with open('res/test.asm', 'r+') as f:
        asm_code = f.read()
          
    executable = assemble(asm_code, SEGMENTS)
    memory.load(executable, DEBUG)
    cpu = CPU(memory, DEBUG)

    while(not cpu.terminated()):
        cpu.run()

    print()