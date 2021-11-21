from GameIDs import ChunkId, NodeId
from Lzo.Lzo import LZO
from Containers import Chunk, Node, Array, List, Vector2, Vector3

from typing import Union
import struct
import logging


class GbxWriter:
    def __init__(self):
        self.data = bytearray()
        self.seen_lookback = False
        self.node_index = 1
        self.stored_strings = []
        self.current_chunk = None
        self.frozen_chunks = []

    def _get_item_by_name(self, name: str, is_ref: bool):
        if is_ref:
            return self.current_chunk[name]
        return name

    def bool(self, name: Union[str, bool], is_ref: bool = True) -> bool:
        """
        Writes a boolean to the buffer (4 bytes)
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        :return: the boolean that got written
        """
        val = self._get_item_by_name(name, is_ref)
        return bool(self.uint32(int(val), is_ref=False))

    def byte(self, name: Union[str, int], is_ref: bool = True) -> bytes:
        """
        Writes a single byte to the buffer
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        :return: the byte that got written
        """
        val = self._get_item_by_name(name, is_ref)
        self.data.extend(bytes([val]))
        return val

    def customArray(self, size: int, arg_list: list, name: Union[str, Array], is_ref: bool = True):
        """
        Writes an array to the buffer
        :param size: length of the array
        :param arg_list: list of tuples (function, name) to specify what's inside each cell
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        """
        array = self._get_item_by_name(name, is_ref)

        for i in range(size):
            d = array.data[i]
            for (f, el_name) in arg_list:
                f(self)(d[el_name], is_ref=False)

    def customList(self, arg_list: list, name: Union[str, List], is_ref: bool = True):
        """
        Writes a list to the buffer
        :param arg_list: list of tuples (function, name) to specify what's inside each cell
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        """
        clist = self._get_item_by_name(name, is_ref)
        self.uint32(clist.size, is_ref=False)
        for i in range(clist.size):
            d = clist.data[i]
            for (f, el_name) in arg_list:
                f(self)(d[el_name], is_ref=False)

    def chunkId(self, name: Union[str, ChunkId], is_ref: bool = True) -> ChunkId:
        """
        Writes a chunkId to the buffer (4 bytes in hexadecimal)
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        :return: the chunkId that got written
        """
        val = self._get_item_by_name(name, is_ref)

        if not isinstance(val, ChunkId):
            logging.error(f"Provided val {val} is not a correct chunkId")
            return ChunkId.Unknown
        val = val.value
        self.data += struct.pack('I', val)
        return val

    def color(self, name: str = None):
        """
        Writes a color to the buffer
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        """
        c = self.current_chunk[name]
        self.float(c.r, is_ref=False)
        self.float(c.g, is_ref=False)
        self.float(c.b, is_ref=False)

    def nodeId(self, name: Union[str, NodeId], is_ref: bool = True) -> NodeId:
        """
        Writes a nodeId to the buffer (4 bytes in hexadecimal)
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        :return: the nodeId that got written
        """
        val = self._get_item_by_name(name, is_ref)

        if not isinstance(val, NodeId):
            logging.error(f"Provided val {val} is not a correct nodeId")
            return NodeId.Unknown
        val = val.value
        self.data += struct.pack('I', val)
        return val

    def fileRef(self, name: str = None):
        """
        Writes a file reference to the buffer
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        """
        file = self.current_chunk[name]
        int(self.byte(file.version, is_ref=False))
        if file.version >= 3:
            self.bytes(32, name=file.checksum, is_ref=False)
        self.string(file.path, is_ref=False)
        if file.path and file.version >= 1:
            self.string(file.locator_url, is_ref=False)

    def float(self, name: Union[str, float], is_ref: bool = True):
        """
        Writes a float to the buffer (4 bytes)
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        """
        val = self._get_item_by_name(name, is_ref)
        self.data.extend(struct.pack('f', val))

    def int16(self, name: Union[str, int], is_ref: bool = True) -> int:
        """
        Writes an int16 to the buffer (2 bytes)
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        :return: the int16 that got written
        """
        val = self._get_item_by_name(name, is_ref)
        self.data.extend(struct.pack('h', val))
        return val

    def int32(self, name: Union[str, int], is_ref: bool = True) -> int:
        """
        Writes an int32 to the buffer (4 bytes)
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        :return: the int32 that got written
        """
        val = self._get_item_by_name(name, is_ref)
        self.data.extend(struct.pack('i', val))
        return val

    def lookbackString(self, name: str, is_ref: bool = True):
        """
        Writes a string with lookback format to the buffer (4 bytes)
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        """
        # TODO: Is setting every lookback string to local name (bit 30 set) sufficient?
        val = self._get_item_by_name(name, is_ref)
        if not self.seen_lookback:
            self.uint32(3, is_ref=False)
            self.seen_lookback = True
        if val == '':
            self.uint32(2 ** 32 - 1, is_ref=False)
        elif val not in self.stored_strings:
            self.uint32(2 ** 30, is_ref=False)
            self.stored_strings.append(val)
            self.string(val, is_ref=False)
        else:
            index = self.stored_strings.index(val) + 1
            self.uint32(2 ** 30 + index, is_ref=False)

    def nodeRef(self, name: str = None):
        """
        Writes a node reference to the buffer
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        """
        node = self.current_chunk[name]
        if node is not None and node.id is not None:
            chunk = self.current_chunk
            # TODO: Figure out how node index really works (sufficient for now)
            self.int32(self.node_index, is_ref=False)
            self.node_index += 1
            self.nodeId(node.id, is_ref=False)
            node_data = self.writeNode(node)
            self.data.extend(node_data)
            self.current_chunk = chunk
        else:
            self.int32(-1, is_ref=False)

    def bytes(self, size: int, name: Union[str, bytes], is_ref: bool = True) -> bytes:
        """
        Writes some bytes to the buffer (4 bytes)
        :param size: unused, kept for compatibility with reading
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        :return: the bytes that got written
        """
        val = self._get_item_by_name(name, is_ref)
        self.data.extend(val)
        return val

    def writeNode(self, node: Node) -> bytes:
        """
        Writes a node to the buffer
        :param node: the node that must be written
        :return: the bytes that got written in the buffer
        """
        pos_before = len(self.data)
        import BlockImporter
        logging.info(f"Node start {node.id}")
        for chunk in node.chunk_list:
            self.chunkId(chunk.id, is_ref=False)

            if BlockImporter.is_skipable(chunk.id):
                logging.info(f"Writing chunk {self.current_chunk.id}")
                chunk_data = self.writeChunk(chunk)
                self.chunkId(ChunkId.Skip, is_ref=False)
                self.uint32(len(chunk_data), is_ref=False)
                self.data.extend(chunk_data)
            elif BlockImporter.is_known(chunk.id):
                logging.info(f"Writing chunk {self.current_chunk.id}")
                chunk_data = self.writeChunk(chunk)
                self.data.extend(chunk_data)
            else:
                logging.warning(f"Unknown chunk {self.current_chunk.id}")

        self.chunkId(ChunkId.Facade, is_ref=False)

        node_data = self.data[pos_before:]
        self.data = self.data[:pos_before]
        return bytes(node_data)

    def resetLookbackState(self):
        """
        Resets the state of the lookback string format. Needed after each header chunk
        """
        self.seen_lookback = False
        self.stored_strings = []

    def saveToFile(self, file: str):
        # TODO : add checks, return success
        """
        Write the current buffer to a file
        :param file: the file where the data needs to be written
        """
        f = open(file, "wb+")
        f.write(bytes(self.data))
        f.close()

    def string(self, name: str, is_ref: bool = True):
        """
        Writes a string to the buffer (size + data)
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        :return: the bytes that got written
        """
        val = self._get_item_by_name(name, is_ref)
        data = bytes(val, 'utf-8')

        self.uint32(len(data), is_ref=False)
        string = struct.pack(f"{len(data)}s", data)
        self.data.extend(string)
        return str(string)

    def uint16(self, name: Union[str, int], is_ref: bool = True) -> int:
        """
        Writes an unsigned int to the buffer (2 bytes)
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        :return: the uint16 that got written
        """
        val = self._get_item_by_name(name, is_ref)
        self.data += struct.pack('H', val)
        return val

    def uint32(self, name: Union[str, int], is_ref: bool = True) -> int:
        """
        Writes an unsigned int to the buffer (4 bytes)
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        :return: the uint32 that got written
        """
        val = self._get_item_by_name(name, is_ref)
        self.data += struct.pack('I', val)
        return val

    def vec2(self, name: Union[str, Vector2], is_ref: bool = True):
        """
        Writes a 2D vector to the buffer (2 * 4 bytes)
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        """
        val = self._get_item_by_name(name, is_ref)
        f1, f2 = val[0], val[1]
        self.float(f1, is_ref=False)
        self.float(f2, is_ref=False)

    def vec3(self, name: Union[str, Vector3], is_ref: bool = True):
        """
        Writes a 3D vector to the buffer (3 * 4 bytes)
        :param name: name of the object inside current chunk. Can be an object if is_ref is False
        :param is_ref: whether name is a reference inside current chunk memory or not (default : true)
        """
        val = self._get_item_by_name(name, is_ref)
        f1, f2, f3 = val[0], val[1], val[2]
        self.float(f1, is_ref=False)
        self.float(f2, is_ref=False)
        self.float(f3, is_ref=False)

    def writeChunk(self, chunk: Chunk) -> bytes:
        """
        Writes a chunk to the buffer
        :param chunk: the chunk that must be written
        :return: the bytes that got written
        """
        import BlockImporter
        self.current_chunk = chunk
        pos_before = len(self.data)
        if BlockImporter.is_known(chunk.id):
            BlockImporter.chunkLink[chunk.id.value](self)
        chunk_data = self.data[pos_before:]
        self.data = self.data[:pos_before]
        return bytes(chunk_data)

    def writeHeader(self, gbx):
        """
        Write the header of the file to the buffer, including the header chunks
        :param gbx: the gbx data from which the header data is taken
        """
        self.bytes(3, b'GBX', is_ref=False)

        version = self.int16(6, is_ref=False)
        self.bytes(3, b'BUC', is_ref=False)
        if version >= 4:
            self.byte(82, is_ref=False)

        if version >= 3:
            self.nodeId(gbx.id, is_ref=False)

        if version >= 6 and not gbx.header_chunk_list:
            self.uint32(0, is_ref=False)
        elif version >= 6:
            chunk_datas = []
            for chunk in gbx.header_chunk_list:
                logging.info(f"Writing chunk {chunk.id}")
                self.resetLookbackState()
                chunk_data = self.writeChunk(chunk)
                chunk_datas.append(chunk_data)

            user_data_size = 4 + sum(len(c) + 8 for c in chunk_datas)  # Chunk + id + size
            self.uint32(user_data_size, is_ref=False)
            self.uint32(len(chunk_datas), is_ref=False)

            for chunk, chunk_data in zip(gbx.header_chunk_list, chunk_datas):
                self.chunkId(chunk.id, is_ref=False)
                # TODO : Figure out real limit for 'heavy chunks'
                if len(chunk_data) < 17000:
                    self.uint32(len(chunk_data), is_ref=False)
                else:
                    self.uint32(len(chunk_data) ^ 1 << 31, is_ref=False)

            for chunk_data in chunk_datas:
                self.data.extend(chunk_data)

    def writeBody(self, gbx):
        """
        Write the body of the file to the buffer, which consists of a compressed main node
        :param gbx: the gbx data from which the body data is taken
        """
        self.uint32(gbx.node_list[0].count_node(), is_ref=False)  # Number of nodes
        self.uint32(0, is_ref=False)  # Number of external nodes
        # TODO : Change gbx.node_list to gbx.main_node
        self.resetLookbackState()
        node_data = self.writeNode(gbx.node_list[0])

        comp_data = LZO().compress(node_data)
        self.uint32(len(node_data), is_ref=False)
        self.uint32(len(comp_data), is_ref=False)
        self.data.extend(comp_data)

    def writeAll(self, gbx):
        """
        Write the whole gbx data to the buffer, header and body
        :param gbx: the gbx data from which the header and body is taken
        """
        self.writeHeader(gbx)
        self.writeBody(gbx)
