"""CGameCtnMediaBlockCameraPath"""


def Chunk002(bp):
    numKeys = bp.uin32('numKeys')
    for i in range(numKeys):
        bp.float(f'timeStamp {i}')
        bp.vec3(f'cameraPosition {i}')
        bp.float(f'pitch {i}')
        bp.float(f'yaw {i}')
        bp.float(f'roll {i}')
        bp.float(f'FOV {i}')
        bp.bool(f'anchorRot {i}')
        bp.uint32(f'idxTargetPlayer {i}')
        bp.bool(f'anchorVis {i}')
        bp.uint32(f'idxAnchorPlayer {i}')
        bp.vec3(f'targetPosition {i}')
        bp.float(f'weight {i}')
        bp.read(4*4, name=f'u1 {i}')
