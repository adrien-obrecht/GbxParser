"""CGameCtnMediaBlockTransitionFade"""


def Chunk000(bp):
    numKeys = bp.uint32('numKeys')
    for i in range(numKeys):
        bp.float(f'timeStamp {i}')
        bp.float(f'opacity {i}')
    bp.vec3(f'transitionColor {i}')
    bp.float('u1')
