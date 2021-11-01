from GbxReader import GbxReader
import Classes.Header as Header


class Gbx:
    def __init__(self, obj):
        self.root_parser = None
        self.d = {}
        if isinstance(obj, str):
            self.f = open(obj, 'rb')
            self.data = self.f.read()
        else:
            self.data = obj

    def parse_all(self):
        self.root_parser = GbxReader(self.data)
        self.root_parser.chunk_order = [0]
        self.d = Header.read_head(self.root_parser)

