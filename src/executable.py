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
        self.labels = {}
        self.variables = {}
        self.statements = {}
        self.statements_raw = {}