"""CGameCtnMediaBlockGhost 030E5"""


def Chunk001(bp):
    bp.float('timeClipStart')
    bp.float('timeClipEnd')
    bp.nodeRef('CGameCtnGhost')
    bp.float('startOffset')


def Chunk002(bp):
    print("chunk002 USED!!")
    version = bp.uint32('version')
    if version > 3:
        bp.float('timeCLipStart')
        bp.float('timeCLipEnd')
    if version >= 3:
        numKeys = bp.uint32('numKeys')
        for i in range(numKeys):
            bp.float(f'timeStamp {i}')
            bp.float(f'u1 {i}')
    bp.nodeRef('ghostModel')
    bp.float('startOffset')
    bp.bool('noDamage')
    bp.bool('forceLight')
    bp.bool('forceHue')