"""CGameCtnMediaBlockFxBlurDepth 03081"""


def Chunk001(bp):
    numKeys = bp.uin32('numKeys')
    for i in range(numKeys):
        bp.float('timeStamp')
        bp.float('lensSize')
        bp.bool('forceFocus')
        bp.float('focusZ')
