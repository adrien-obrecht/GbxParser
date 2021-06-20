"""CGameControlCameraFree"""


def Chunk003(bp):
    bp.float('timeClipStart')
    bp.float('timeClipEnd')
    bp.lookbackString('cameraView')
    bp.uint32('idxTargetPlayer')

