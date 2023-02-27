from src.executable import Executable
from src.assembler import assemble
from src.memory import Memory

MEMORY_SIZE = int('FFFFF', 16)  # 1  MB
SEGMENT_SIZE = int('10000', 16) # 64 KB

# default offsets
SEGMENTS = {
    'CS': int('1000', 16),
    'DS': int('2000', 16),
    'SS': int('3000', 16),
    'ES': int('4000', 16),
}

if __name__ == "__main__":
    memory = Memory(SEGMENT_SIZE, MEMORY_SIZE)

    with open('res/test.asm', 'r+') as f:
        asm_code = f.read()
          
    executable = assemble(asm_code, SEGMENTS)
    # memory.load(executable)
    print()