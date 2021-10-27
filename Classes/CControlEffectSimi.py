"""CControlEffectSimi 07010"""


def Chunk003(bp):
    numKeys = bp.uint32('numKeys')
    for i in range(numKeys):
        bp.float(f'timeStamp {i}')
        bp.vec2(f'position {i}')
        bp.float(f'rotation {i}')
        bp.float(f'scaleX {i}')
        bp.float(f'scaleY {i}')
        bp.float(f'opacity {i}')
        bp.float(f'depth {i}')
    bp.bool('centered')


def Chunk005(bp):
    numKeys = bp.uint32('numKeys')
    for i in range(numKeys):
        bp.float(f'timeStamp {i}')
        bp.vec2(f'position {i}')
        bp.float(f'rotation {i}')
        bp.float(f'scaleX {i}')
        bp.float(f'scaleY {i}')
        bp.float(f'opacity {i}')
        bp.float(f'depth {i}')
        bp.float(f'u1 {i}')
        bp.float(f'isContinuous {i}')
        bp.float(f'u2 {i}')
        bp.float(f'u3 {i}')
    bp.bool('centered')
    bp.uint32('colorBlendMode')
    bp.bool('isContinuousEffect')
    bp.bool('isInterpolated')