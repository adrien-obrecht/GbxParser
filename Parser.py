from enum import IntEnum

from GbxReader import GbxReader
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
        self.root_parser.chunkOrder = [0]
        self.d = Header.readHead(self.root_parser)

