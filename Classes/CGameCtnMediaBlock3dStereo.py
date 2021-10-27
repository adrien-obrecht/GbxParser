"""CGameCtnMediaBlock3dStereo 03024"""


def Chunk000(bp):
    numKeys = bp.uin32('numKeys')
    for i in range(numKeys):
        bp.float(f'timeStamp {i}')
        bp.float(f'separation {i}')
        bp.float(f'screenDist {i}')