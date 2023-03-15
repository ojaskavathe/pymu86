class Executable(object):
    def __init__(
        self, 
        segments: dict[str, int]
    ) -> None:
        self.ip: int = 0                                        # instruction pointer
        self.segment_space: dict[str, list] = {}                # {'DS': [[0x24], [0], ... ], 'CS': [['MOV', 'AX', 'DATA'], ... ], ... }
        self.segment_addressability: dict[str, str] = {}        # {'CODE': 'CS', 'DATA': 'DS'}
        self.segment_lengths: dict[str, int] = {}               # {'DS': 9, 'CS': 14, ... }
        self.segment_address: dict[str, str] = {
            'CS': hex(segments['CS']),
            'DS': hex(segments['DS']),
            'SS': hex(segments['SS']),
            'ES': hex(segments['ES'])
        }
        self.labels: dict[str, dict] = {}                       # {'START': {'seg': '0x1000', 'offset': '0x0'}, ... }
        self.variables: dict[str, dict] = {}                    # {'ARR': {'seg': '0x2000', 'offset': '0x0'}, ... }
        self.statements: list[list[str]] = {}
        self.statements_raw: list[str] = {}