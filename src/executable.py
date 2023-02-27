class Executable(object):
    def __init__(
        self, 
        segments: dict[str, int]
    ) -> None:
        self.ip = 0                             # instruction pointer
        self.segment_space = {}                 # {'DS': [[0x24], [0], ... ], 'CS': [['MOV', 'AX', 'DATA'], ... ], ... }
        self.segment_addressability = {}        # {'CODE': 'CS', 'DATA': 'DS'}
        self.segment_lengths = {}               # {'DS': 9, 'CS': 14, ... }
        self.segment_addresses = {
            'CS': hex(segments['CS']),
            'DS': hex(segments['DS']),
            'SS': hex(segments['SS']),
            'ES': hex(segments['ES'])
        }
        self.labels = {}                        # {'START': {'segment_address': '0x1000', 'offset': '0x0'}, ... }
        self.variables = {}                     # {'ARR': {'segment_address': '0x2000', 'offset': '0x0'}, ... }
        self.statements = {}
        self.statements_raw = {}