import struct


class GbxWriter:
    def __init__(self):
        self.data = bytearray()
        self.seen_lookback = False
        self.value_handler = {}
        self.chunk_order = []
        self.node_names = {}
        self.node_index = 1
        self.stored_strings = []
        self.current_chunk = None

    def __repr__(self):
        return self.data.hex()

    def uint32(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(struct.pack('I', val))
        return val

    def int32(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(struct.pack('i', val))

    def bool(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        if val:
            return self.uint32(1, isRef=False)
        else:
            return self.uint32(0, isRef=False)

    def uint16(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(struct.pack('H', val))
        return val

    def int16(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(struct.pack('h', val))
        return val

    def int8(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(struct.pack('b', val))

    def float(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(struct.pack('f', val))

    def vec2(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        f1, f2 = val[0], val[1]
        self.float(f1, isRef=False)
        self.float(f2, isRef=False)

    def vec3(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        f1, f2, f3 = val[0], val[1], val[2]
        self.float(f1, isRef=False)
        self.float(f2, isRef=False)
        self.float(f3, isRef=False)

    def read(self, size, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(val)
        return val

    def string(self, name, decode=True, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name

        if decode:
            self.uint32(len(bytes(val, 'utf-8')), isRef=False)
            self.data.extend(struct.pack(f"{len(bytes(val, 'utf-8'))}s", bytes(val, 'utf-8')))
            return struct.pack(f"{len(bytes(val, 'utf-8'))}s", bytes(val, 'utf-8'))
        else:
            self.uint32(len(val), isRef=False)
            self.read(0, name)

    def lookbackString(self, name, isRef=True, gameStrings=False):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        if not self.seen_lookback:
            self.uint32(3, isRef=False)
            self.seen_lookback = True
        if val == '':
            self.uint32(2 ** 32 - 1, isRef=False)
        else:
            self.uint32(2**30, isRef=False)
            self.string(val, isRef=False)

    def byte(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(bytes([val]))
        return val

    def readNode(self):
        import BlockImporter
        cC = self.current_chunk
        print(f"Node start {cC if cC is None else hex(cC)}")
        while True:
            self.current_chunk = self.chunk_order[0]
            self.chunk_order = self.chunk_order[1:]
            self.uint32(self.current_chunk, isRef=False)

            if self.current_chunk == 0xFACADE01:
                self.current_chunk = cC
                print("Encountered FACADE, end of node")
                return

            if self.current_chunk in BlockImporter.skipableChunkList:
                print(f"Writing chunk {hex(self.current_chunk)}")
                sData = self.data
                self.data = bytearray()
                BlockImporter.chunkLink[self.current_chunk](self)
                nData = self.data
                self.data = sData
                self.uint32(0x534B4950, isRef=False)
                self.uint32(len(nData), isRef=False)
                self.data.extend(nData)
            elif self.current_chunk in BlockImporter.chunkLink:
                print(f"Writing chunk {hex(self.current_chunk)}")
                BlockImporter.chunkLink[self.current_chunk](self)
            else:
                print(f"Unknown chunk {hex(self.current_chunk)}")
                return

    def nodeRef(self, name=None):
        vH = self.value_handler
        self.value_handler = self.value_handler[self.current_chunk][name]
        if self.value_handler is not None:
            self.int32(self.node_index, isRef=False)
            self.node_index += 1
            self.uint32(self.node_names[name], isRef=False)
            self.readNode()
        else:
            self.int32(-1, isRef=False)
        self.value_handler = vH

    def fileRef(self, name=None):
        val = self.value_handler[self.current_chunk][name]
        version = self.byte(val['version'], isRef=False)
        if version >= 3:
            self.read(32, name=val['checksum'], isRef=False)
        filePath = self.string(val['filePath'], isRef=False)
        if len(filePath) > 0 and version >= 1:
            self.string(val['locatorUrl'], isRef=False)
