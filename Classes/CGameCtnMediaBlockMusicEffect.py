"""CGameCtnMediaBlockMusicEffect 030A6"""


def Chunk001(bp):
    numKeys = bp.uint32('numKeys')
    for i in range(numKeys):
        bp.float(f'timeStamp {i}')
        bp.float(f'musicVolume {i}')
        bp.float(f'soundVolume {i}')