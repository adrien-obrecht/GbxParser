import struct
import logging


class GbxWriter:
    def __init__(self):
        self.data = bytearray()
        self.seen_lookback = False
        self.value_handler = {}
        self.chunk_order = []
        self.node_index = 1
        self.stored_strings = []
        self.current_chunk = None
        self.frozen_chunks = []

    def __repr__(self):
        return self.data.hex()

    def bool(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        if val:
            return self.uint32(1, isRef=False)
        else:
            return self.uint32(0, isRef=False)

    def byte(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(bytes([val]))
        return val

    def fileRef(self, name=None):
        val = self.value_handler[self.current_chunk][name]
        version = self.byte(val['version'], isRef=False)
        if version >= 3:
            self.read(32, name=val['checksum'], isRef=False)
        filePath = self.string(val['filePath'], isRef=False)
        if len(filePath) > 0 and version >= 1:
            self.string(val['locatorUrl'], isRef=False)

    def float(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(struct.pack('f', val))

    def freezeCurrentChunk(self):
        d = {'data': self.data, 'current_chunk': self.current_chunk}
        self.frozen_chunks.append(d)

    def int16(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(struct.pack('h', val))
        return val

    def int32(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(struct.pack('i', val))

    def int8(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(struct.pack('b', val))

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

    def nodeRef(self, name=None):
        vH = self.value_handler
        if self.value_handler[self.current_chunk][name] is not None:
            self.int32(self.node_index, isRef=False)
            self.node_index += 1
            self.uint32(self.value_handler[self.current_chunk][name + "Id"], isRef=False)
            self.value_handler = self.value_handler[self.current_chunk][name]
            self.readNode()
        else:
            self.int32(-1, isRef=False)
        self.value_handler = vH

    def read(self, size, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(val)
        return val

    def readNode(self):
        import BlockImporter
        cC = self.current_chunk
        logging.info(f"Node start {cC if cC is None else hex(cC)}")
        while True:
            self.current_chunk = self.chunk_order[0]
            self.chunk_order = self.chunk_order[1:]
            self.uint32(self.current_chunk, isRef=False)

            if self.current_chunk == 0xFACADE01:
                self.current_chunk = cC
                logging.info("Encountered FACADE, end of node")
                return

            if self.current_chunk in BlockImporter.skipableChunkList:
                logging.info(f"Writing chunk {hex(self.current_chunk)}")
                sData = self.data
                self.data = bytearray()
                BlockImporter.chunkLink[self.current_chunk](self)
                nData = self.data
                self.data = sData
                self.uint32(0x534B4950, isRef=False)
                self.uint32(len(nData), isRef=False)
                self.data.extend(nData)
            elif self.current_chunk in BlockImporter.chunkLink:
                logging.info(f"Writing chunk {hex(self.current_chunk)}")
                BlockImporter.chunkLink[self.current_chunk](self)
            else:
                logging.info(f"Unknown chunk {hex(self.current_chunk)}")
                return

    def resetLookbackState(self):
        self.seen_lookback = False
        self.stored_strings = []

    def saveToFile(self, file: str) -> ():
        f = open(file, "wb+")
        f.write(bytes(self.data))
        f.close()

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

    def uint16(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(struct.pack('H', val))
        return val

    def uint32(self, name, isRef=True):
        if isRef:
            val = self.value_handler[self.current_chunk][name]
        else:
            val = name
        self.data.extend(struct.pack('I', val))
        return val

    def unfreezeCurrentChunk(self):
        if not self.frozen_chunks:
            logging.warning("No chunks where frozen")
            return
        d = self.frozen_chunks.pop()
        self.data = d['data']
        self.current_chunk = d['current_chunk']

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

    def writeAll(self):
        import BlockImporter
        self.current_chunk = 0
        BlockImporter.chunkLink[0](self)
