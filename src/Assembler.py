class Assembler(object):
    def __init__(self, segments):
        self.segment_addresses = {
            'CS': hex(segments['CS']),
            'DS': hex(segments['DS']),
            'SS': hex(segments['SS']),
            'ES': hex(segments['ES'])
        }
    