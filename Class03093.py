"""CGameCtnReplayRecord"""

from pygbx import Gbx


def Chunk000(bp):
    version = bp.uint32('version')
    if version >= 2:
        trackUID = bp.lookbackString()
        environment = bp.lookbackString()
        author = bp.lookbackString()
        bp.uint32('time')
        bp.string('nickname')
        if version >= 6:
            bp.string('driverLogin')
            bp.byte()
            titleUID = bp.lookbackString()


def Chunk001(bp):
    bp.string(decode=False)  # XML


def Chunk002(bp):
    GBXSize = bp.uint32('GBXSize')
    data = bytes(bp.read(GBXSize))
    try:
        track = Gbx(data)
    except Exception as e:
        print(f'Failed to parse map data: {e}')


def Chunk007(bp):
    bp.uint32()


def Chunk014(bp):
    bp.skip(4)
    num_ghosts = bp.array('subNode')
