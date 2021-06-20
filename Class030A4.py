"""CGameCtnMediaBlockCameraEffectShake"""


def Chunk000(bp):
    numKeys = bp.uint32('numKeys')
    for i in range(numKeys):
        bp.float(f'timeStamp {i}')
        bp.float(f'intensity {i}')
        bp.float(f'speed {i}')