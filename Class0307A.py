"""CGameCtnMediaClipGroup"""


def Chunk003(bp):
    bp.uint32('u1')
    numClips = bp.uint32('numClips')
    for i in range(numClips):
        bp.nodeRef(f'clip {i}')
    numClips = bp.uint32('numClips')
    for i in range(numClips):
        bp.vec3(f'refFramePos {i}')
        bp.uint32(f'refFrameRot {i}')
        bp.uint32(f'triggerCondition {i}')
        bp.float(f'triggerArgument {i}')
        numTriggers = bp.uint32(f'rnumTriggers {i}')
        for j in range(numTriggers):
            bp.vec3(f'position {i} {j}')
