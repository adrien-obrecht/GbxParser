from ChunkID import Id
from Containers import Array, Vector2, Vector3, List
from collections import OrderedDict
import logging
import os

import struct


class GbxReader:
    def __init__(self, data):
        if os.path.isfile(data):
            f = open(data, 'rb')
            self.data = f.read()
        else:
            self.data = data
        self.pos = 0
        self.frozen_chunks = []
        self.seen_lookback = False
        self.lookback_history = []
        self.node_index = set()
        self.stored_strings = []
        self.value_handler = OrderedDict()
        self.chunk_value = {}
        self.chunk_order = []

    def bool(self, name=None):
        val = self.uint32() == 1

        if name is not None:
            self.chunk_value[name] = val
        return val

    def byte(self, name=None):
        """Reads a single byte from the buffer.
        Returns:
            the single byte read from the buffer
        """
        val = self.data[self.pos]
        self.pos += 1
        if name is not None:
            self.chunk_value[name] = val
        return val

    def customArray(self, length, arg_list, name=None):
        l = Array()
        for _ in range(length):
            d = {}
            for (f, el_name) in arg_list:
                d[el_name] = f(self)()
            l.add(d)
        if name is not None:
            self.chunk_value[name] = l
        return l

    def customList(self, arg_list, name=None):
        l = List()
        length = self.uint32()
        for _ in range(length):
            d = {}
            for (f, el_name) in arg_list:
                d[el_name] = f(self)()
            l.add(d)
        if name is not None:
            self.chunk_value[name] = l
        return l

    def chunkId(self, name=None):
        val = self.read(4, 'I')
        if not Id.intIsId(val):
            logging.error(f"Unknown chunkId {val}")
            return
        chunkId = Id(val)
        if name is not None:
            self.chunk_value[name] = chunkId
        return chunkId

    def color(self, name=None):
        val = self.float(), self.float(), self.float()

        if name is not None:
            self.chunk_value[name] = val
        return val

    def fileRef(self, name=None):
        version = self.byte()
        if version >= 3:
            checkSum = self.read(32)
        else:
            checkSum = None

        filePath = self.string()
        if len(filePath) > 0 and version >= 1:
            locatorUrl = self.string()
        else:
            locatorUrl = None

        if name is not None:
            self.chunk_value[name] = {'version': version, 'checksum': checkSum, 'filePath': filePath,
                                      'locatorUrl': locatorUrl}
        return checkSum, filePath, locatorUrl

    def float(self, name=None):
        """Reads a 32 bit float.

        Returns:
            the float read from the buffer
        """
        val = self.read(4, 'f')
        if name is not None:
            self.chunk_value[name] = val
        return val

    def freezeCurrentChunk(self):
        d = {'data': self.data, 'pos': self.pos, 'chunk_value': self.chunk_value}
        self.chunk_value = {}
        self.frozen_chunks.append(d)

    def int16(self, name=None):
        """Reads a signed int16.

        Returns:
            the integer read from the buffer
        """
        val = self.read(2, 'h')
        if name is not None:
            self.chunk_value[name] = val
        return val

    def int32(self, name=None):
        """Reads a signed int32.

        Returns:
            the integer read from the buffer
        """
        val = self.read(4, 'i')
        if name is not None:
            self.chunk_value[name] = val
        return val

    def int8(self, name=None):
        """Reads a signed int8.

        Returns:
            the integer read from the buffer
        """
        val = self.read(1, 'b')
        if name is not None:
            self.chunk_value[name] = val
        return val

    def lookbackString(self, name=None):
        if not self.seen_lookback:
            self.uint32()
        self.seen_lookback = True

        inp = self.uint32()
        b31 = (inp >> 30) & 1
        b32 = (inp >> 31) & 1
        index = inp & 0x3fffffff

        if not (b31 or b32):
            logging.error("Unhandled case! CollectionId not finished.")
            s = index
        elif b31 ^ b32:
            if index == 0:
                s = self.string()
                self.stored_strings.append(s)
            else:
                s = self.stored_strings[index - 1]
        else:
            s = ''
        self.lookback_history.append([bin(inp), s])
        if name is not None:
            self.chunk_value[name] = s
        return s

    def nodeRef(self, name=None):
        idx = self.int32()
        if idx >= 0 and idx not in self.node_index:
            id = self.chunkId()
            self.chunk_value[name + "Id"] = id
            self.node_index.add(idx)
            cV = self.chunk_value
            vH = self.value_handler
            self.value_handler = {}
            self.readNode()
            vH, self.value_handler = self.value_handler, vH
            self.chunk_value = cV
            val = vH
        else:
            val = None

        if name is not None:
            self.chunk_value[name] = val
        return val

    def parseAll(self):
        import Classes.Header
        self.chunk_order = [0]
        Classes.Header.readHead(self)

    def read(self, num_bytes, typestr=None, name=None):
        val = bytes(self.data[self.pos:self.pos + num_bytes])
        self.pos += num_bytes
        if typestr is not None:
            try:
                val = struct.unpack(typestr, val)[0]
            except Exception as e:
                logging.error(e)
                return 0

        if name is not None:
            self.chunk_value[name] = val
        return val

    def readNode(self):
        import BlockImporter
        while True:
            self.chunk_value = {}
            chunkId = self.chunkId()
            self.chunk_order.append(chunkId)
            if chunkId == Id['Facade']:
                return
            skipsize = -1
            skip = self.int32()
            if skip == 0x534B4950:
                if chunkId.value not in BlockImporter.skipableChunkList:
                    logging.error(f"Chunk {chunkId} should be in skipableChunkList!")
                skipsize = self.uint32()
            else:
                self.pos -= 4
            if chunkId.value in BlockImporter.chunkLink:
                logging.info(f"Reading chunk {chunkId}")
                BlockImporter.chunkLink[chunkId.value](self)
                self.value_handler[chunkId] = self.chunk_value
            elif skipsize != -1:
                logging.info(f"Skiping chunk {chunkId}")
                self.skip(skipsize)
            else:
                logging.info(f"Unknown chunk {chunkId}")
                return

    def resetLookbackState(self):
        self.seen_lookback = False
        self.stored_strings = []

    def skip(self, num_bytes):
        """Skips provided amount of bytes in the buffer
        Args:
            num_bytes (int): the number of bytes to skip
        """
        self.pos += num_bytes

    def storeCurrentChunk(self, name):
        self.value_handler[name] = self.chunk_value

    def string(self, name=None, decode=True):
        """Reads a string from the buffer, first reading the length, then it's data.
        Returns:
            the string read from the buffer, None if there was an error
        """
        strlen = self.uint32()
        try:
            if not decode:
                val = self.read(strlen)
            else:
                val = self.read(strlen, str(strlen) + 's').decode('utf-8')

        except UnicodeDecodeError as e:
            logging.warning(f'Failed to read string: {e}')
            val = None

        if name is not None:
            self.chunk_value[name] = val
        return val

    def uint16(self, name=None):
        """Reads an unsigned int16.

        Returns:
            the integer read from the buffer
        """
        val = self.read(2, 'H')
        if name is not None:
            self.chunk_value[name] = val
        return val

    def uint32(self, name=None):
        """Reads an unsigned int32.

        Returns:
            the integer read from the buffer
        """
        val = self.read(4, 'I')
        if name is not None:
            self.chunk_value[name] = val
        return val

    def unfreezeCurrentChunk(self):
        if not self.frozen_chunks:
            logging.warning("No chunks where frozen")
            return
        d = self.frozen_chunks.pop()
        self.data = d['data']
        self.pos = d['pos']
        self.chunk_value = d['chunk_value']

    def vec2(self, name=None):
        val = Vector2(self.float(), self.float())

        if name is not None:
            self.chunk_value[name] = val
        return val

    def vec3(self, name=None):
        val = Vector3(self.float(), self.float(), self.float())

        if name is not None:
            self.chunk_value[name] = val
        return val
