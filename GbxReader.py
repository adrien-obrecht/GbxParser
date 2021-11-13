from GameIDs import ChunkId, NodeId
from Containers import Array, Vector2, Vector3, List, Node, Chunk
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
        self.value_handler = Node()
        self.value_handler.id = NodeId.Main
        self.chunk_value = Node()
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
        if not ChunkId.intIsId(val):
            logging.error(f"Unknown chunk Id {val}")
            return
        chunk_id = ChunkId(val)
        if name is not None:
            self.chunk_value[name] = chunk_id
        return chunk_id

    def color(self, name=None):
        val = self.float(), self.float(), self.float()

        if name is not None:
            self.chunk_value[name] = val
        return val

    def fileRef(self, name=None):
        version = self.byte()
        if version >= 3:
            check_sum = self.read(32)
        else:
            check_sum = None

        file_path = self.string()
        if len(file_path) > 0 and version >= 1:
            locator_url = self.string()
        else:
            locator_url = None

        if name is not None:
            self.chunk_value[name] = {'version': version,
                                      'checksum': check_sum,
                                      'filePath': file_path,
                                      'locatorUrl': locator_url}
        return check_sum, file_path, locator_url

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
        self.chunk_value = Node()
        self.chunk_value.depth = d['chunk_value'].depth + 1
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

    def nodeId(self, name=None):
        val = self.read(4, 'I')
        if not NodeId.intIsId(val):
            logging.error(f"Unknown node Id {val}")
            return
        node_id = NodeId(val)
        if name is not None:
            self.chunk_value[name] = node_id
        return node_id

    def nodeRef(self, name=None):
        index = self.int32()
        if index >= 0 and index not in self.node_index:
            id = self.nodeId()
            self.node_index.add(index)
            former_chunk_value = self.chunk_value
            former_value_handler = self.value_handler
            self.value_handler = Node()
            self.value_handler.id = id
            self.value_handler.depth = former_value_handler.depth + 1
            self.readNode()
            node = self.value_handler
            self.value_handler = former_value_handler
            self.chunk_value = former_chunk_value
        else:
            node = None

        if name is not None:
            self.chunk_value[name] = node
        return node

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
        depth = self.chunk_value.depth
        while True:
            self.chunk_value = Chunk()
            self.chunk_value.depth = depth
            chunk_id = self.chunkId()
            self.chunk_value.id = chunk_id
            self.chunk_order.append(chunk_id)
            if chunk_id == ChunkId['Facade']:
                return
            skip_size = -1
            skip = self.int32()
            if skip == 0x534B4950:
                if chunk_id.value not in BlockImporter.skipableChunkList:
                    logging.error(f"Chunk {chunk_id} should be in skipableChunkList!")
                skip_size = self.uint32()
            else:
                self.pos -= 4
            if chunk_id.value in BlockImporter.chunkLink:
                logging.info(f"Reading chunk {chunk_id}")
                BlockImporter.chunkLink[chunk_id.value](self)
                self.value_handler[chunk_id] = self.chunk_value
            elif skip_size != -1:
                logging.info(f"Skipping chunk {chunk_id}")
                self.skip(skip_size)
            else:
                logging.info(f"Unknown chunk {chunk_id}")
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
        str_len = self.uint32()
        try:
            if not decode:
                val = self.read(str_len)
            else:
                val = self.read(str_len, str(str_len) + 's').decode('utf-8')

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
