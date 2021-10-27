from enum import IntEnum

from ByteReader import ByteReader
import Classes.Header as Header


class GbxType(IntEnum):
    """Represents the type of the main or auxiliary class contained within the GBX file.
    Some classes may have a different or multiple ID's, depending on what version of the GBX file is being parsed.
    """
    CHALLENGE = 0x03043000
    CHALLENGE_OLD = 0x24003000
    COLLECTOR_LIST = 0x0301B000
    CHALLENGE_PARAMS = 0x0305B000
    BLOCK_SKIN = 0x03059000
    WAYPOINT_SPECIAL_PROP = 0x0313B000
    ITEM_MODEL = 0x2E002000
    REPLAY_RECORD = 0x03093000
    REPLAY_RECORD_OLD = 0x02407E000
    GAME_GHOST = 0x0303F005
    CTN_GHOST = 0x03092000
    CTN_GHOST_OLD = 0x2401B000
    CTN_COLLECTOR = 0x0301A000
    CTN_OBJECT_INFO = 0x0301C000
    CTN_DECORATION = 0x03038000
    CTN_COLLECTION = 0x03033000
    GAME_SKIN = 0x03031000
    GAME_PLAYER_PROFILE = 0x0308C000
    MW_NOD = 0x01001000
    UNKNOWN = 0x0


class GbxLoadError(Exception):
    """Thrown when the Gbx class fails to parse the provided Gbx object"""

    def __init__(self, message):
        """Initializes the Exception instance with a message.
        Args:
            message (str): the message
        """
        self.message = message


class Gbx(object):
    """The Gbx class provides the main interface for parsing GBX files and retrieving data
    that is contained within these files. The class provides support primarily for parsing Challenges and Replays.
    The class should properly support most TMNF/TMUF files, with support for some TM2 files.
    It is not guaranteed that the class will parse all of the data in a GBX file. If an error is encountered,
    an error will be logged with the logging module, but the class will attempt to read until the end of the file, unless
    the file is not a GBX file, then a GbxLoadError is thrown.
    The class uses the ByteReader class which provides support for reading data types exposed by the GBX file format,
    found on https://wiki.xaseco.org/wiki/GBX.
    If the class does not provide support for reading a chunk you want to specifically read, use find_raw_chunk_id
    to obtain access to a ByteReader with the cursor positioned at the beggining of provided chunk ID.
    """

    def __init__(self, obj):
        """Creates the main Gbx instance from a file path or from bytes object.
        Parses the Gbx file sequentially, reading all supported chunks until no more chunks have
        been found. Parsing can fail depending on the what classes or chunks it contains and what
        version of the GBX file is being parsed. 
        Args:
            obj (str/bytes): a file path to the Gbx file or bytes object containing the Gbx data
        Raises:
            GbxLoadError: raised when the supplied object is not a GBX file or data
        """
        if isinstance(obj, str):
            self.f = open(obj, 'rb')
            self.root_parser = ByteReader(self.f)
        else:
            self.root_parser = ByteReader(obj)

        self.root_parser.chunkOrder = [0]
        self.d = Header.readHead(self.root_parser)
"""
        self.magic = self.root_parser.read(3, '3s')
        if self.magic.decode('utf-8') != 'GBX':
            raise GbxLoadError(f'obj is not a valid Gbx data: magic string is incorrect')
        self.version = self.root_parser.read(2, 'H')
        self.classes = {}
        self.root_classes = {}
        self.positions = {}
        self.__current_class = None
        self.__current_waypoint = None
        self.__replay_header_info = {}

        self.root_parser.skip(3)
        if self.version >= 4:
            self.root_parser.skip(1)

        if self.version >= 3:
            self.class_id = self.root_parser.uint32()
            try:
                self.type = GbxType(self.class_id)
            except ValueError:
                self.type = GbxType.UNKNOWN

            if self.version >= 6:
                self._read_user_data()

            self.num_nodes = self.root_parser.uint32()

        self.num_external_nodes = self.root_parser.uint32()
        if self.num_external_nodes > 0:
            print("Num external node is not 0! ")

        self.root_parser.push_info()
        self.positions['data_size'] = self.root_parser.pop_info()

        data_size = self.root_parser.uint32()
        compressed_data_size = self.root_parser.uint32()
        cdata = self.root_parser.read(compressed_data_size)
        self.data = bytearray(lzo.decompress(cdata, False, data_size))

        bp = ByteReader(self.data)
        bp.valueHandler = self.root_parser.valueHandler
        bp.chunkOrder = self.root_parser.chunkOrder
        self.root_parser = bp
        self.root_parser.readNode()

    def _read_user_data(self):
        entries = {}

        self.root_parser.push_info()
        self.user_data_size = self.root_parser.uint32()
        self.positions['user_data_size'] = self.root_parser.pop_info()

        user_data_pos = self.root_parser.pos
        num_chunks = self.root_parser.uint32()
        for _ in range(num_chunks):
            if self.root_parser.pos >= self.root_parser.size - 1:
                self.root_parser.pos = user_data_pos + self.user_data_size
                return

            cid = self.root_parser.uint32()
            self.root_parser.push_info()
            size = self.root_parser.uint32()
            self.positions[str(cid)] = self.root_parser.pop_info()
            entries[cid] = size

        for cid, size in entries.items():
            self.root_parser.chunkValue = {}
            if cid in bi.chunkLink:
                print(f"Reading chunk {hex(cid)}")
                bi.chunkLink[cid](self.root_parser)
                self.root_parser.chunkOrder.append(cid)
                self.root_parser.valueHandler[cid] = self.root_parser.chunkValue
            else:
                print(f"Skiping chunk {hex(cid)}")
                self.root_parser.skip(size)

        self.root_parser.pos = user_data_pos + self.user_data_size
"""