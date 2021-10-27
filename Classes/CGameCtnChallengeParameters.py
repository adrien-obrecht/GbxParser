"""CGameCtnChallengeParameters 0305B"""


def Chunk001(bp):
    bp.string('tip1')
    bp.string('tip2')
    bp.string('tip3')
    bp.string('tip4')


def Chunk004(bp):
    bp.uint32('bronzeTime')
    bp.uint32('silverTime')
    bp.uint32('goldTIme')
    bp.uint32('authorTime')
    bp.uint32('u1')


def Chunk008(bp):
    bp.uint32('timeLimit')
    bp.uint32('authorScore')

