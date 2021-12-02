"""CSystemConfig 0B005"""
import binascii


def Chunk008(bp):
    bp.string('language')


def Chunk009(bp):
    bp.bytes(24, name='u1')


def Chunk00B(bp):
    bp.uint32('u1')
    bp.uint32('u2')
    bp.uint32('u3')
    bp.uint32('u4')


def Chunk020(bp):
    # TODO : This is a 0-noderef (extension of current object) that needs to be implemented
    bp.bytes(4, name='u1')


def Chunk02B(bp):
    bp.uint32('u1')
    bp.uint32('u2')
    bp.uint32('u3')


def Chunk030(bp):
    bp.uint32('u1')
    bp.uint32('u2')
    bp.uint32('u3')
    bp.uint32('u4')
    bp.uint32('u5')
    bp.uint32('u6')
    bp.uint32('u7')
    bp.uint32('u8')
    bp.uint32('u9')
    bp.uint32('u10')


def Chunk034(bp):
    bp.uint32('u1')
    bp.uint32('u2')
    bp.uint32('u3')
    bp.uint32('u4')
    bp.uint32('u5')
    bp.uint32('u6')
    bp.uint32('u7')


def Chunk039(bp):
    bp.bytes(12, name='u1')
    bp.uint32('port1')  # TCP and UDP (see https://www.speedguide.net/port.php?port=2350)
    bp.uint32('port2')  # TCP (see https://www.speedguide.net/port.php?port=3450)
    bp.uint32('u4')
    bp.uint32('u5')
    bp.uint32('u6')
    bp.string('ip')
    bp.bytes(12, name='ipMask')


def Chunk03A(bp):
    bp.bytes(20, name='u1')


def Chunk03E(bp):
    bp.bytes(24, name='u1')


def Chunk041(bp):
    bp.uint32('u1')


def Chunk044(bp):
    bp.uint32('u1')
    bp.string('mainServerURL')
    bp.string('subCategory')
    size = bp.uint32('size')
    for i in range(size):
        bp.bytes(4, name=f'u2{i}')


def Chunk045(bp):
    bp.bytes(16, name='u1')


def Chunk047(bp):
    bp.bytes(4, name=f'u1')


def Chunk048(bp):
    bp.uint32('u1')
    bp.string('USer')


def Chunk049(bp):
    bp.bytes(8, name=f'u1')


def Chunk04A(bp):
    bp.bytes(12, name=f'u1')
    bp.uint32('u2')
    bp.uint32('u3')


def Chunk04C(bp):
    bp.uint32('u1')
    bp.uint32('u2')


def Chunk04D(bp):
    bp.bytes(16, name=f'u1')


def Chunk04E(bp):
    size = bp.uint32('size')
    for i in range(size):
        bp.string(f'u{i}')


def Chunk04F(bp):
    bp.uint32('u1')
    bp.float('u2')
    bp.float('u3')
    bp.uint32('u4')
    bp.uint32('u5')
    bp.uint32('u6')
    bp.uint32('u7')
    bp.uint32('u8')
    bp.uint32('u9')
    bp.uint32('u10')
    bp.string('u11')
