from GameIDs import ChunkId, NodeId
from Containers import Array, Vector2, Vector3, List, Node, Chunk, File, Color
from Gbx import Gbx
from Lzo.Lzo import LZO

import logging
import os
import struct


class GbxReader:
    """
    arg1 : data, can be a path to a file or a simple string of data

    This object is used to read each SampleGbxFiles datatype (see https://wiki.xaseco.org/wiki/GBX#Primitives for more info)
    It holds some local chunk values, and can therefore add each read values to it's internal memory, if a name is
    provided for it.
    """

    def __init__(self, data: str):
        if os.path.isfile(data):
            f = open(data, 'rb')
            self.data = f.read()
        else:
            self.data = data
        self.pos = 0
        self.gbx = None
        self.frozen_chunks = []
        self.seen_lookback = False
        self.node_index = {}
        self.stored_strings = []
        self.current_chunk = Chunk()

    def bool(self, name=None) -> bool:
        """
        Reads a bool (4 bytes) from the buffer
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the bool that was read
        """
        val = self.uint32() == 1

        if name is not None:
            self.current_chunk[name] = val
        return val

    def byte(self, name=None) -> str:
        """
        Reads a byte from the buffer
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the byte that was read, as string
        """
        val = self.data[self.pos]
        self.pos += 1
        if name is not None:
            self.current_chunk[name] = val
        return val

    def customArray(self, length: int, arg_list: list, name=None) -> Array:
        """
        Reads an array from the buffer
        :param length: number of elements in the array
        :param arg_list: in the form of tuples (function, name) to specify the data inside each cell
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the array that was read
        """
        array = Array()
        for _ in range(length):
            d = {}
            for (f, el_name) in arg_list:
                d[el_name] = f(self)()
            array.add(d)
        if name is not None:
            self.current_chunk[name] = array
        return array

    def customList(self, arg_list: list, name=None) -> List:
        """
        Reads a list from the buffer (size then data)
        :param arg_list: in the form of tuples (function, name) to specify the data inside each cell
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the list that was read
        """
        clist = List()
        length = self.uint32()
        for _ in range(length):
            d = {}
            for (f, el_name) in arg_list:
                d[el_name] = f(self)()
            clist.add(d)
        if name is not None:
            self.current_chunk[name] = clist
        return clist

    def chunkId(self, name=None) -> ChunkId:
        """
        Reads a chunkId from the buffer (4 bytes hex)
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the chunkId that was read (ChunkId.Unknown if unknown, which can cause problems)
        """
        val = self.bytes(4, 'I')
        if not ChunkId.intIsChunkId(val):
            return ChunkId.Unknown
        chunk_id = ChunkId(val)
        if name is not None:
            self.current_chunk[name] = chunk_id
        return chunk_id

    def color(self, name=None) -> Color:
        """
        Reads a color from the buffer (3 floats)
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the color that was read
        """
        c = Color()
        c.r, c.g, c.b = self.float(), self.float(), self.float()

        if name is not None:
            self.current_chunk[name] = c
        return c

    def fileRef(self, name=None) -> File:
        """
        Reads a file from the buffer (version, checksum, path, url)
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the file that was read
        """
        f = File()
        f.version = int(self.byte())
        if f.version >= 3:
            f.check_sum = self.bytes(32)

        f.path = self.string()
        if f.path and f.version >= 1:
            f.locator_url = self.string()

        if name is not None:
            self.current_chunk[name] = f
        return f

    def float(self, name=None) -> float:
        """
        Reads a float (4 bytes)
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the float that was read
        """
        val = self.bytes(4, 'f')
        if name is not None:
            self.current_chunk[name] = val
        return val

    def freezeCurrentChunk(self):
        """
        Stores the current chunk context, to read a subnode
        """
        self.frozen_chunks.append(self.current_chunk)
        self.current_chunk = Chunk()

    def int16(self, name=None) -> int:
        """
        Reads a signed integer (2 bytes)
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: The int16 that was read
        """
        val = self.bytes(2, 'h')
        if name is not None:
            self.current_chunk[name] = val
        return val

    def int32(self, name=None):
        """
        Reads a signed integer (4 bytes)
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: The int32 that was read
        """
        val = self.bytes(4, 'i')
        if name is not None:
            self.current_chunk[name] = val
        return val

    def lookbackString(self, name=None) -> str:
        """
        Reads a string with the lookback format, adding it to the lookback table
        (see https://wiki.xaseco.org/wiki/ManiaPlanet_internals#Id for more details)
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the string that was read
        """

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
        if name is not None:
            self.current_chunk[name] = s
        return s

    def nodeId(self, name=None) -> NodeId:
        """
        Reads a nodeId from the buffer (4 bytes hex)
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the nodeId that was read (ChunkId.Unknown if unknown, which can cause problems)
        """
        val = self.bytes(4, 'I')
        if not NodeId.intIsNodeId(val):
            logging.error(f"Unknown node Id {val}")
            return NodeId.Unknown
        node_id = NodeId(val)
        if name is not None:
            self.current_chunk[name] = node_id
        return node_id

    def nodeRef(self, name=None) -> Node:
        """
        Reads a sub-node from the buffer
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the node that was read
        """
        index = self.int32()
        if index >= 0 and index not in self.node_index:
            id = self.nodeId()
            self.freezeCurrentChunk()
            node = self.readNode()
            node.id = id
            self.node_index[index] = node
            self.unfreezeCurrentChunk()
        elif index in self.node_index:
            node = self.node_index[index]
        else:
            node = Node()

        if name is not None:
            self.current_chunk[name] = node
        return node

    def bytes(self, num_bytes: int, format_str: str = None, name=None):
        """
        Reads any specified number of bytes from the buffer, with a special format if specified
        :param num_bytes: number of bytes to read
        :param format_str: format of the unpacked data (default are raw bytes)
        (see https://docs.python.org/3/library/struct.html#struct-format-strings for more details)
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the data that was read, in the format specified by format_str
        """
        val = bytes(self.data[self.pos:self.pos + num_bytes])
        self.pos += num_bytes
        if format_str is not None:
            try:
                val = struct.unpack(format_str, val)[0]
            except Exception as e:
                logging.error(e)
                return ''

        if name is not None:
            self.current_chunk[name] = val
        return val

    def readChunk(self, id: ChunkId) -> Chunk:
        """
        Reads a chunk from the buffer (as a SampleGbxFiles datatype)
        :param id: ChunkId needed to properly parse the chunk
        :return: the chunk that was read
        """
        import BlockImporter
        self.current_chunk = Chunk()
        self.current_chunk.id = id
        if BlockImporter.is_known(id):
            BlockImporter.chunkLink[id.value](self)
        return self.current_chunk

    def readNode(self) -> Node:
        """
        Reads a node from the buffer
        :return: the node that was read
        """
        node = Node()
        import BlockImporter
        while True:
            id = self.chunkId()
            if id == ChunkId.Facade:
                return node
            skip_size = -1
            skip = self.chunkId()
            if skip == ChunkId.Skip:
                if not BlockImporter.is_skippable(id):
                    logging.error(f"Chunk {id} should be in skippableChunkList!")
                skip_size = self.uint32()
            else:
                self.pos -= 4
            if BlockImporter.is_known(id):
                logging.info(f"Reading chunk {id}")
                chunk = self.readChunk(id)
                node.chunk_list.append(chunk)
            elif skip_size != -1:
                logging.info(f"Skipping chunk {id}")
                self.skip(skip_size)
            else:
                logging.error(f"Unknown chunk {id}")
                return node

    def resetLookbackState(self):
        """
        Resets the lookbackstring state, needed at the beginning of each new header chunk
        """
        self.seen_lookback = False
        self.stored_strings = []

    def skip(self, num_bytes: int):
        """
        Skips a specified number of bytes in the buffer
        :param num_bytes: number of bytes to skip
        """
        self.pos += num_bytes

    def string(self, name=None) -> str:
        """
        Reads a string from the buffer (size then data)
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the string that was read
        """
        str_len = self.uint32()
        try:
            val = self.bytes(str_len, str(str_len) + 's').decode('utf-8')

        except UnicodeDecodeError as e:
            logging.warning(f'Failed to read string: {e}')
            val = ''

        if name is not None:
            self.current_chunk[name] = val
        return val

    def uint16(self, name=None) -> int:
        """
        Reads an unsigned integer (2 bytes)
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: The uint16 that was read
        """
        val = self.bytes(2, 'H')
        if name is not None:
            self.current_chunk[name] = val
        return val

    def uint32(self, name=None):
        """
        Reads an unsigned integer (4 bytes)
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: The uint32 that was read
        """
        val = self.bytes(4, 'I')
        if name is not None:
            self.current_chunk[name] = val
        return val

    def unfreezeCurrentChunk(self):
        """
        Loads back a chunk that was previously frozen, ex after a noderef
        """
        if not self.frozen_chunks:
            logging.warning("No chunks were frozen!")
            return Chunk()
        self.current_chunk = self.frozen_chunks.pop()

    def vec2(self, name=None) -> Vector2:
        """
        Reads a vector2 from the buffer (float, float)
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the vector2 that was read
        """
        val = Vector2(self.float(), self.float())

        if name is not None:
            self.current_chunk[name] = val
        return val

    def vec3(self, name=None):
        """
        Reads a vector3 from the buffer (float, float, float)
        :param name: name of the variable if wanted to be saved in memory (default is None)
        :return: the vector3 that was read
        """
        val = Vector3(self.float(), self.float(), self.float())

        if name is not None:
            self.current_chunk[name] = val
        return val

    def readHeader(self):
        """
        Reads the header of the file with which the GbxReader was initialized
        """
        magic = self.bytes(3)

        if magic.decode('utf-8') != 'GBX':
            logging.warning("Not a SampleGbxFiles file!")
            return

        version = self.int16()
        compression = self.bytes(3)
        if version >= 4:
            self.byte('u2')

        if version >= 3:
            self.gbx.id = self.nodeId()

        if version >= 6:
            user_data_size = self.uint32()
            if user_data_size:
                entries = self.customList([(lambda x: x.chunkId, 'id'),
                                           (lambda x: x.uint32, 'size')])
                for c in entries:
                    size, id = c['size'], c['id']
                    self.resetLookbackState()
                    if id != ChunkId.Unknown:
                        logging.info(f"Reading chunk {id}")
                        self.readChunk(id)
                        self.gbx.header_chunk_list.append(self.current_chunk)
                    else:
                        logging.warning(f"Skipping chunk {id}")
                        self.skip(size)

    def readBody(self):
        """
        Reads the body of the file with which the GbxReader was initialized
        """
        num_nodes = self.uint32()

        num_external_nodes = self.uint32()

        if num_external_nodes > 0:
            logging.warning(f"Num external node is {num_external_nodes}! ")

        # TODO : Find files with uncompressed data to properly handle them

        data_size = self.uint32()
        comp_data_size = self.uint32()
        import binascii
        self.gbx.raw_data = binascii.hexlify(self.data[:self.pos])
        self.gbx.raw_data += bytes("AAAAAAAA", 'utf-8')
        comp_data = self.bytes(comp_data_size)

        if comp_data_size <= 0:
            return

        self.resetLookbackState()

        self.data = LZO().decompress(comp_data, data_size)

        self.gbx.raw_data += binascii.hexlify(self.data)

        self.pos = 0
        node = self.readNode()
        node.id = NodeId.Body
        self.gbx.main_node = node

    def readAll(self) -> Gbx:
        """
        Reads the whole file with which the GbxReader was initialized
        :return: all the data that was read
        """
        self.gbx = Gbx()
        self.readHeader()
        self.readBody()
        return self.gbx
