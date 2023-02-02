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
    with open('res/test.asm', 'r+') as f:
        asm_code = f.read()

    print(asm_code)
    # assembler = Assembler()
    # executable = assembler.compile(asm)
    # memory.load(executable)