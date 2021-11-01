import logging
import struct
from Headers import Vector3, Vector2


class GbxReader:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.seen_loopback = False
        self.node_index = set()
        self.stored_strings = []
        self.node_names = {}
        self.value_handler = {}
        self.chunk_value = {}
        self.chunk_order = []

    def readNode(self):
        import BlockImporter
        while True:
            self.chunk_value = {}
            chunkId = self.uint32()
            self.chunk_order.append(chunkId)
            if chunkId == 0xFACADE01:
                return
            skipsize = -1
            skip = self.int32()
            if skip == 0x534B4950:
                skipsize = self.uint32()
            else:
                self.pos -= 4
            if chunkId in BlockImporter.chunkLink:
                print(f"Reading chunk {hex(chunkId)}")
                BlockImporter.chunkLink[chunkId](self)
                self.value_handler[chunkId] = self.chunk_value
            elif skipsize != -1:
                print(f"Skiping chunk {hex(chunkId)}")
                self.skip(skipsize)
            else:
                print(f"Unknown chunk {hex(chunkId)}")
                return

    def nodeRef(self, name=None):
        idx = self.int32()
        if idx >= 0 and idx not in self.node_index:
            self.node_names[name] = self.uint32()
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
            self.chunk_value[name] = {'version' : version, 'checksum': checkSum, 'filePath': filePath, 'locatorUrl': locatorUrl}
        return checkSum, filePath, locatorUrl

    def int32(self, name=None):
        """Reads a signed int32.

        Returns:
            the integer read from the buffer
        """
        val = self.read(4, 'i')
        if name is not None:
            self.chunk_value[name] = val
        return val

    def bool(self, name=None):
        val = self.uint32() == 1

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

    def int16(self, name=None):
        """Reads a signed int16.

        Returns:
            the integer read from the buffer
        """
        val = self.read(2, 'h')
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

    def int8(self, name=None):
        """Reads a signed int8.

        Returns:
            the integer read from the buffer
        """
        val = self.read(1, 'b')
        if name is not None:
            self.chunk_value[name] = val
        return val

    def float(self, name=None):
        """Reads a 32 bit float.

        Returns:
            the float read from the buffer
        """
        val = self.read(4, 'f')
        if name is not None:
            self.chunk_value[name] = val
        return val

    def vec3(self, name=None):
        val = Vector3(self.float(), self.float(), self.float())

        if name is not None:
            self.chunk_value[name] = val
        return val

    def vec2(self, name=None):
        val = Vector2(self.float(), self.float())

        if name is not None:
            self.chunk_value[name] = val
        return val

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
            print(f'Failed to read string: {e}')
            val = None

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

    def skip(self, num_bytes):
        """Skips provided amount of bytes in the buffer
        Args:
            num_bytes (int): the number of bytes to skip
        """
        self.pos += num_bytes

    def lookbackString(self, name=None, gameStrings=False):
        """Reads a special string type in the GBX file format called the lookbackstring.

        Such type is used to reference already read strings, or introduce them if they were not
        read yet. A ByteReader instance keeps track of lookback strings previously read and
        returns an already existing string, if the data references it. For more information,
        see the lookbackstring type in the GBX file format: https://wiki.xaseco.org/wiki/GBX.
        Returns:
            the lookback string read from the buffer
        """
        def aux(self, name, gameStrings):
            if not self.seen_loopback:
                self.uint32()

            self.seen_loopback = True
            inp = self.uint32()
            if (inp & 0xc0000000) != 0 and (inp & 0x3fffffff) == 0:
                s = self.string()
                self.stored_strings.append(s)
                return s

            if inp == 0:
                s = self.string()
                self.stored_strings.append(s)
                return s

            if inp == -1:
                return ''

            if (inp & 0x3fffffff) == inp:
                if inp == 11:
                    return 'Valley'
                elif inp == 12:
                    return 'Canyon'
                elif inp == 13:
                    return 'Lagoon'
                elif inp == 17:
                    return 'TMCommon'
                elif inp == 202:
                    return 'Storm'
                elif inp == 299:
                    return 'SMCommon'
                elif inp == 10003:
                    return 'Common'

            inp &= 0x3fffffff
            if inp - 1 >= len(self.stored_strings):
                return ''
            return self.stored_strings[inp - 1]

        val = aux(self, name, gameStrings)

        if name is not None:
            self.chunk_value[name] = val
        return val
