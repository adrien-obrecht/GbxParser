"""CGameCtnMediaBlockGhost"""


def Chunk001(bp):
    bp.float('timeClipStart')
    bp.float('timeClipEnd')
    bp.nodeRef('CGameCtnGhost')
    bp.float('startOffset')