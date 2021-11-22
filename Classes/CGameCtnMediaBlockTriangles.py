"""CGameCtnMediaBlockTriangles 03029"""


def Chunk001(bp):
    # TODO : implement smth for array of arrays
    bp.customList([(lambda x: x.float, 'time')],
                  'time_stamps')
    numKeys = bp.uint32('numKeys')
    numPoints = bp.uint32('numPoints')
    for i in range(numKeys):
        bp.customArray(numPoints,
                       [(lambda x: x.vec3, 'position')],
                       f'point_positions {i}')
    bp.customList([(lambda x: x.color, 'color'),
                   (lambda x: x.float, 'opacity')],
                  'color_info')
    bp.customList([(lambda x: x.uint32, 'vertex 1'),
                   (lambda x: x.uint32, 'vertex 2'),
                   (lambda x: x.uint32, 'vertex 3')],
                  'triangles')
    bp.bytes(7 * 4, name='u1')
