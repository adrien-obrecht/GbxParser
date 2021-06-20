"""CGameCtnChallenge"""


def Chunk002(bp):
    version = bp.byte('version')
    if version < 3:
        bp.lookbackString('id')
        bp.lookbackString('collection')
        bp.lookbackString('author')
        bp.string('trackname')
    bp.bool('u1')
    if version >= 1:
        bp.int32('bronzeTime')
        bp.int32('silverTime')
        bp.int32('goldTime')
        bp.int32('authorTime')
        if version == 2:
            bp.byte('u2')
        if version >= 4:
            bp.uint32('cost')
            if version >= 5:
                bp.uint32('multilap')
                if version == 6:
                    bp.bool('u3')
                if version >= 7:
                    bp.uint32('trackType')
                    if version >= 9:
                        bp.uint32('u4')
                        if version >= 10:
                            bp.uint32('authorScore')
                            if version >= 11:
                                bp.uint32('editorMode')
                                if version >= 12:
                                    bp.bool('u5')
                                    if version >= 13:
                                        bp.uint32('nbCheckpoints')
                                        bp.uint32('nbLaps')


def Chunk003(bp):
    version = bp.byte('version')
    bp.lookbackString('trackUID')
    bp.lookbackString('environment')
    bp.lookbackString('mapAuthor')
    bp.string('trackName')
    bp.byte('kind')
    if version >= 1:
        bp.bool('locked')
        bp.string('password')
        if version >= 2:
            bp.lookbackString('timeOfDay')
            bp.lookbackString('envirDecoration')
            bp.lookbackString('envirAuthor')
            if version >= 3:
                bp.vec2('mapOrigin')
                if version >= 4:
                    bp.vec2('mapTarget')
                    if version >= 5:
                        bp.read(16, name='u1')
                        if version >= 6:
                            bp.string('mapType')
                            bp.string('mapStyle')
                            if version <= 8:
                                bp.bool('u2')
                            if version >= 8:
                                bp.read(8, name='lightmapCacheUID')
                                if version >= 9:
                                    bp.byte('lightmapVersion')
                                    if version >= 11:
                                        bp.lookbackString('titleUID')


def Chunk004(bp):
    bp.uint32('version')


def Chunk005(bp):
    bp.string('XML', decode=False)


def Chunk007(bp):
    version = bp.uint32('version')
    if version != 0:
        size = bp.uint32('size')
        bp.read(len("<Thumbnail.jpg>"), name="<Thumbnail.jpg>")
        bp.read(size, name='Thumbnail')
        bp.read(len("</Thumbnail.jpg>"), name="</Thumbnail.jpg>")
        bp.read(len("<Comments>"), name="<Comments>")
        bp.string('commments')
        bp.read(len("</Comments>"), name="</Comments>")


def Chunk00D(bp):
    bp.lookbackString('vehicle')
    bp.lookbackString('collection')
    bp.lookbackString('author')


def Chunk011(bp):
    bp.nodeRef('collectorList')
    bp.nodeRef('challengeParameters')
    bp.uint32('kind')


def Chunk017(bp):
    #bp.array('checkPoints',
    #         [(lambda x: x.uint32(), 'cp1'),
    #          (lambda x: x.uint32(), 'cp2'),
    #          (lambda x: x.uint32(), 'cp3')])
    numCheckpoints = bp.uint32('numCheckpoints')
    for i in range(numCheckpoints):
        bp.uint32(f'Cp {i} 1')
        bp.uint32(f'Cp {i} 2')
        bp.uint32(f'Cp {i} 3')


def Chunk018(bp):
    bp.bool('u1')
    bp.uint32('numLaps')


def Chunk019(bp):
    bp.fileRef('modPackDesc')


def Chunk01C(bp):
    bp.uint32('playMode')


def Chunk01F(bp):
    bp.lookbackString('trackUID')
    bp.lookbackString('environment')
    bp.lookbackString('mapAuthor')
    bp.string('trackName')
    bp.lookbackString('timeOfDay')
    bp.lookbackString('envirDecoration')
    bp.lookbackString('envirAuthor')
    bp.uint32('sizeX')
    bp.uint32('sizeY')
    bp.uint32('sizeZ')
    bp.bool('needUnlock')
    version = bp.uint32('version')
    numBlocks = bp.uint32('numBlocks')
    for i in range(numBlocks):
        bp.lookbackString(f'blockName {i}')
        bp.byte(f'rotation {i}')
        bp.byte(f'posX {i}')
        bp.byte(f'posY {i}')
        bp.byte(f'posZ {i}')
        if version == 0:
            flags = bp.uint16(f'flags {i}')
        if version > 0:
            flags = bp.uint32(f'flags {i}')
        if flags == 0xFFFFFFFF:
            continue
        if flags & 0x8000 != 0:
            bp.lookbackString(f'author {i}')
            bp.nodeRef(f'skin {i}')
        if flags & 0x100000:
            bp.nodeRef(f'blockParameters {i}')


def Chunk021(bp):
    bp.nodeRef('clipIntro')
    bp.nodeRef('clipGroupInGame')
    bp.nodeRef('clipGroupEndRace')


def Chunk022(bp):
    bp.uint32('u1')


def Chunk024(bp):
    bp.fileRef('customMusicPackDesc')


def Chunk025(bp):
    bp.vec2('mapCoordOrigin')
    bp.vec2('mapCoordTarget')


def Chunk026(bp):
    bp.nodeRef('clipGlobal')


def Chunk028(bp):
    archiveGmCamVal = bp.bool('archiveGmCamVal')
    if archiveGmCamVal:
        bp.byte('u1')
        bp.vec3('mat1')
        bp.vec3('mat2')
        bp.vec3('mat3')
        bp.vec3('u2')
        bp.float('u3')
        bp.float('u4')
        bp.float('u5')
    bp.string('comments')


def Chunk029(bp):
    bp.read(16, name='passwordHash')

    bp.uint32('CRC32')


def Chunk02A(bp):
    bp.bool('u1')
