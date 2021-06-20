import logging
import struct
from io import IOBase
from Headers import Vector3, Vector2
from os import SEEK_END


class PositionInfo(object):
    """
    This classes holds information that is mainly private to
    the Gbx class but can still be retrieved through the positions member.
    The PositionInfo marks a specific section in the file through it's position and size.
    """

    def __init__(self, pos, size):
        """Constructs a new PositionInfo"""

        self.pos = pos
        self.size = size

    @property
    def valid(self):
        """Checks if the instance of the section is valid

        Returns:
            True if the instance points to a valid section in the file, False otherwise
        """
        return self.pos > -1 and self.size > 0


class ByteReader(object):
    """The ByteReader class is used by the Gbx class to read specific data types supported by the GBX file format.
    The class provides convinience methods for reading raw types such as integers, strings and vectors, which
    are the main data types of the GBX file format. While reading the file, the Gbx class may instantiate multiple
    instances of ByteReader to read different parts of the file. This is because some chunks depend on the state
    of the reader, this state can be e.g: lookback strings.
    ByteReader accepts reading from raw bytes as well as from a file handle.
    """

    def __init__(self, obj):
        """Constructs a new ByteReader with the provided object.
        Args:
            obj (file/bytes): a file handle opened through open() or a bytes object
        """
        self.data = obj
        if isinstance(obj, IOBase):
            self.get_bytes = self.__get_bytes_file
            self.data.seek(0, SEEK_END)
            self.size = self.data.tell()
            self.data.seek(0)
        else:
            self.get_bytes = self.__get_bytes_generic
            self.size = len(self.data)

        self.pos = 0
        self.seen_loopback = False
        self.nodeIndexes = set()
        self.stored_strings = []
        self.nodeNames = {}
        self.current_info = PositionInfo(-1, 0)
        self.valueHandler = {}
        self.chunkValue = {}
        self.chunkOrder = []

    def readNode(self):
        import BlockImporter
        while True:
            self.chunkValue = {}
            chunkId = self.uint32()
            self.chunkOrder.append(chunkId)
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
                self.valueHandler[chunkId] = self.chunkValue
            elif skipsize != -1:
                print(f"Skiping chunk {hex(chunkId)}")
                self.skip(skipsize)
            else:
                print(f"Unknown chunk {hex(chunkId)}")
                return

    def nodeRef(self, name=None):
        idx = self.int32()
        if idx >= 0 and idx not in self.nodeIndexes:
            self.nodeNames[name] = self.uint32()
            self.nodeIndexes.add(idx)
            cV = self.chunkValue
            vH = self.valueHandler
            self.valueHandler = {}
            self.readNode()
            vH, self.valueHandler = self.valueHandler, vH
            self.chunkValue = cV
            val = vH
        else:
            val = None

        if name is not None:
            self.chunkValue[name] = val
        return val

    def read(self, num_bytes, typestr=None, name=None):
        """Reads an arbitrary amount of bytes from the buffer.
        Reads the buffer of length num_bytes and optionally
        takes a type string that is passed to struct.unpack if not None.
        Args:
            num_bytes (int): the number of bytes to read from the buffer
            typestr (str): the format character used by the struct module, passing None does not unpack the bytes

        Returns:
            the bytes object, if no type string was provided, type returned by struct.unpack otherwise
        """
        val = self.get_bytes(num_bytes)
        self.pos += num_bytes
        if typestr is not None:
            try:
                val = struct.unpack(typestr, val)[0]
            except Exception as e:
                logging.error(e)
                return 0

        if name is not None:
            self.chunkValue[name] = val
        return val

    def color(self, name=None):
        val = self.float(), self.float(), self.float()

        if name is not None:
            self.chunkValue[name] = val
        return val

    def readable(self, size):
        import binascii
        return binascii.hexlify(self.read(size))

    def array(self, varType):
        size = self.uint32()
        array = []
        for _ in range(size):
            if varType == 'uint32':
                array.append(self.uint32())
            elif varType == 'nodeRef':
                array.append(self.nodeRef())
            elif varType == 'fileRef':
                array.append(self.fileRef())
            elif varType == 'lookbackString':
                array.append(self.lookbackString())
            elif varType == 'byte':
                array.append(self.byte())
        return array

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
            self.chunkValue[name] = {'version' : version, 'checksum': checkSum, 'filePath': filePath, 'locatorUrl': locatorUrl}
        return checkSum, filePath, locatorUrl

    def size(self):
        if isinstance(self.data, IOBase):
            return self.data.tell()
        else:
            return len(self.data)

    def __get_bytes_file(self, num_bytes):
        self.data.seek(self.pos)
        return self.data.read(num_bytes)

    def __get_bytes_generic(self, num_bytes):
        return bytes(self.data[self.pos:self.pos + num_bytes])

    def int32(self, name=None):
        """Reads a signed int32.

        Returns:
            the integer read from the buffer
        """
        val = self.read(4, 'i')
        if name is not None:
            self.chunkValue[name] = val
        return val

    def bool(self, name=None):
        val = self.uint32() == 1

        if name is not None:
            self.chunkValue[name] = val
        return val

    def uint32(self, name=None):
        """Reads an unsigned int32.

        Returns:
            the integer read from the buffer
        """
        val = self.read(4, 'I')
        if name is not None:
            self.chunkValue[name] = val
        return val

    def int16(self, name=None):
        """Reads a signed int16.

        Returns:
            the integer read from the buffer
        """
        val = self.read(2, 'h')
        if name is not None:
            self.chunkValue[name] = val
        return val

    def uint16(self, name=None):
        """Reads an unsigned int16.

        Returns:
            the integer read from the buffer
        """
        val = self.read(2, 'H')
        if name is not None:
            self.chunkValue[name] = val
        return val

    def int8(self, name=None):
        """Reads a signed int8.

        Returns:
            the integer read from the buffer
        """
        val = self.read(1, 'b')
        if name is not None:
            self.chunkValue[name] = val
        return val

    def float(self, name=None):
        """Reads a 32 bit float.

        Returns:
            the float read from the buffer
        """
        val = self.read(4, 'f')
        if name is not None:
            self.chunkValue[name] = val
        return val

    def vec3(self, name=None):
        val = Vector3(self.float(), self.float(), self.float())

        if name is not None:
            self.chunkValue[name] = val
        return val

    def vec2(self, name=None):
        val = Vector2(self.float(), self.float())

        if name is not None:
            self.chunkValue[name] = val
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
            logging.error(f'Failed to read string: {e}')
            return None

        if name is not None:
            self.chunkValue[name] = val
        return val

    def byte(self, name=None):
        """Reads a single byte from the buffer.
        Returns:
            the single byte read from the buffer
        """
        val = self.get_bytes(1)[0]
        self.pos += 1
        if name is not None:
            self.chunkValue[name] = val
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
        if not self.seen_loopback:
            self.uint32()
            self.seen_loopback = True
        val = None

        inp = self.uint32()
        if (inp & 0xc0000000) != 0 and (inp & 0x3fffffff) == 0:
            s = self.string()
            self.stored_strings.append(s)
            val = s

        elif inp == 0:
            s = self.string()
            self.stored_strings.append(s)
            val = s

        elif inp == -1:
            val = ''

        elif (inp & 0x3fffffff) == inp:
            if inp == 11:
                val = 'Valley'
            elif inp == 12:
                val = 'Canyon'
            elif inp == 13:
                val = 'Lagoon'
            elif inp == 17:
                val = 'TMCommon'
            elif inp == 202:
                val = 'Storm'
            elif inp == 299:
                val = 'SMCommon'
            elif inp == 10003:
                val = 'Common'

        elif inp & 0x3fffffff - 1 >= len(self.stored_strings):
            val = ''

        elif val is None:
            val = self.stored_strings[inp & 0x3fffffff - 1]

        if name is not None:
            self.chunkValue[name] = val
        return val
