"""CGameCtnMediaBlockTime 03085"""


def Chunk000(bp):
    numKeys = bp.uint32('numKeys')
    for i in range(numKeys):
        bp.float(f'timeStamp {i}')
        bp.float(f'timeValue {i}')
        bp.float(f'tangent {i}')
