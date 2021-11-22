"""CGameCtnReplayRecord 03093 """


def Chunk000(bp):
    version = bp.uint32('version')
    if version >= 2:
        bp.lookbackString('trackUID')
        bp.lookbackString('environment')
        bp.lookbackString('author')
        bp.uint32('time')
        bp.string('nickname')
        if version >= 6:
            bp.string('driverLogin')
            if version >= 8:
                bp.byte('u1')
                bp.lookbackString('titleUID')


def Chunk001(bp):
    bp.string('XML')


def Chunk002(bp):
    GBXSize = bp.uint32('GBXSize')
    bp.bytes(GBXSize, name='data')
    """data = bytes(bp.read(GBXSize, 'data'))
    try:
        track = GbxReader(data)
    except Exception as e:
        print(f'Failed to parse map data: {e}')"""


def Chunk007(bp):
    bp.uint32('u1')


def Chunk014(bp):
    bp.uint32('version')
    numGhosts = bp.uint32('numGhosts')
    for i in range(numGhosts):
        bp.nodeRef(f'ghost {i}')
    bp.bytes(4, name='u1')
    num_extras = bp.uint32('num_extras')
    for i in range(num_extras):
        bp.uint32(f"extra 1 {i}")
        bp.uint32(f"extra 2 {i}")


def Chunk015(bp):
    bp.nodeRef('clip')

