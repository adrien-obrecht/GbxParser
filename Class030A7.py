"""CGameCtnMediaBlockSound"""


def Chunk001(bp):
    bp.fileRef('sound')
    numKeys = bp.uint32('numKeys')
    for i in range(numKeys):
        bp.float('timeStamp')
        bp.float('volume')
        bp.float('pan')


def Chunk002(bp):
    bp.uint32('playCount')
    bp.bool('isLooping')


def Chunk003(bp):
    version = bp.uint32('version')
    bp.uint32('playCount')
    bp.bool('isLooping')
    bp.bool('isMusic')
    if version >= 1:
        bp.bool('stopWithClip')
        if version >= 2:
            bp.bool('audiotToSpeech')
            bp.bool('audioToSpeechTarget')


def Chunk004(bp):
    bp.fileRef('sound')
    bp.uint32('u1')
    numKeys = bp.uint32('numKeys')
    for i in range(numKeys):
        bp.float(f'timeStamp {i}')
        bp.float(f'volume {i}')
        bp.float(f'pan {i}')
        bp.vec3(f'soundTransmitorPosition {i}')