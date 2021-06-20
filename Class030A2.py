"""CGameCtnMediaBlockCameraCustom"""


def Chunk005(bp):
    numKeys = bp.uint32('numKeys')
    for i in range(numKeys):
        bp.float(f'timStamp {i}')
        bp.uint32(f'interpolation {i}')
        bp.read(8, name=f'u1 {i}')
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
        bp.float(f'leftTangentX {i}')
        bp.float(f'leftTangentY {i}')
        bp.float(f'leftTangentZ {i}')
        bp.float(f'rightTangentX {i}')
        bp.float(f'rightTangentY {i}')
        bp.float(f'rightTangentZ {i}')
