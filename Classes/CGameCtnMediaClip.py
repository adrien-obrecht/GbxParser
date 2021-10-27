"""CGameCtnMediaClip 03079"""


def Chunk004(bp):
    bp.uint32('u1')


def Chunk005(bp):
    bp.uint32('u1')
    numTracks = bp.uint32('numTracks')
    for i in range(numTracks):
        bp.nodeRef(f'mediaTrack {i}')
    bp.string('clipName')


def Chunk007(bp):
    bp.uint32('localPlayerClipEntIndex')


