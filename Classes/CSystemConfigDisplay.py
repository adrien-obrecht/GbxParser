"""CSystemConfigDisplay 0B013"""


def Chunk001(bp):
    bp.uint32('resolutionX')
    bp.uint32('resolutionY')
    bp.uint32('u3')
    bp.uint32('u4')
    bp.uint32('u5')
    bp.uint32('u6')
    bp.uint32('u7')
    bp.uint32('u8')


def Chunk003(bp):
    bp.uint32('u1')
    bp.uint32('u2')
    bp.uint32('u3')
    bp.uint32('u4')
    bp.uint32('u5')
    bp.uint32('u6')


def Chunk004(bp):
    bp.uint32('u1')


def Chunk005(bp):
    bp.uint32('u1')


def Chunk008(bp):
    bp.uint32('u1')
    bp.uint32('u2')
    bp.uint32('u3')


def Chunk009(bp):
    bp.uint32('u1')
    bp.uint32('u2')
    bp.uint32('u3')
    bp.uint32('u4')


def Chunk00A(bp):
    bp.uint32('u1')
    bp.uint32('u2')


def Chunk00B(bp):
    bp.uint32('u1')
    bp.float('u2')


def Chunk00F(bp):
    bp.uint32('u1')


def Chunk010(bp):
    bp.float('u1')


def Chunk011(bp):
    bp.uint32('u1')


def Chunk013(bp):
    bp.uint32('u1')


def Chunk015(bp):
    bp.uint32('u1')


def Chunk016(bp):
    bp.uint32('u1')


def Chunk017(bp):
    bp.uint32('u1')


def Chunk018(bp):
    bp.uint32('u1')


def Chunk019(bp):
    bp.uint32('u1')


def Chunk01B(bp):
    bp.uint32('u1')


def Chunk01C(bp):
    bp.uint32('u1')
    bp.uint32('u2')


def Chunk01D(bp):
    bp.uint32('u1')


def Chunk01E(bp):
    bp.uint32('u1')


def Chunk020(bp):
    bp.uint32('u1')
    bp.uint32('u2')


def Chunk021(bp):
    bp.uint32('u1')


def Chunk022(bp):
    bp.uint32('u1')
    bp.uint32('u2')
    bp.uint32('u3')
    bp.uint32('u4')
    bp.uint32('u5')
    bp.uint32('u6')
    bp.uint32('u7')

    bp.uint32('FIXME (FACADE)')
