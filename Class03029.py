"""CGameCtnMediaBlockTriangles"""


def Chunk001(bp):
    numKeys = bp.uint32('numKeys')
    for i in range(numKeys):
        bp.float(f'timeStamp {i}')
    numKeys = bp.uint32('numKeys')
    numPoints = bp.uin32('numPoints')
    for i in range(numKeys):
        for j in range(numPoints):
            bp.vec3(f'pointPosition {i} {j}')
    numPoints = bp.uint32('numPoints')
    for i in range(numPoints):
        bp.vec3(f'pointColor {i}')
        bp.float(f'opacity {i}')
    numTriangles = bp.uint32('numTriangles')
    for i in range(numTriangles):
        bp.uint32(f'vertex1 {i}')
        bp.uint32(f'vertex2 {i}')
        bp.uint32(f'vertex3 {i}')
    bp.read(7*4, name='u1')
