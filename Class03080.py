"""CGameCtnMediaBlockFxColors"""


def Chunk003(bp):
    numKeys = bp.uint32('numKeys')
    for i in range(numKeys):
        bp.float(f'timeStamp {i}')
        bp.float(f'intensity {i}')
        bp.float(f'blendZ {i}')
        bp.float(f'distance near {i}')
        bp.float(f'distance far {i}')
        for j in ('near', 'far'):
            bp.float(f'inverse {i} {j}')
            bp.float(f'hue {i} {j}')
            bp.float(f'saturation {i} {j}')
            bp.float(f'brightness {i} {j}')
            bp.float(f'contrast {i} {j}')
            bp.vec3(f'color {i} {j}')
            bp.read(4*4, name=f'u1 {i} {j}')