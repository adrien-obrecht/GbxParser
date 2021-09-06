"""CGameCtnReplayRecord"""


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
    bp.string(decode=False, name='XML')  # XML


def Chunk002(bp):
    from Parser import Gbx
    GBXSize = bp.uint32('GBXSize')
    bp.read(GBXSize, name='data')
    """data = bytes(bp.read(GBXSize, 'data'))
    try:
        track = Gbx(data)
    except Exception as e:
        print(f'Failed to parse map data: {e}')"""


def Chunk007(bp):
    bp.uint32('u1')


def Chunk014(bp):
    bp.read(4, name='u1')
    numGhosts = bp.uint32('numGhosts')
    for i in range(numGhosts):
        bp.nodeRef(f'ghost {i}')
    bp.read(16, name='u2')
