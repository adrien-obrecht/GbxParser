"""CGameCtnGhost 03092"""


def Chunk005(bp):
    bp.uint32('raceTime')


def Chunk008(bp):
    bp.uint32('numRespawns')


def Chunk009(bp):
    bp.color('lightTrailColor')


def Chunk00A(bp):
    bp.uint32('stuntsScore')


def Chunk00B(bp):
    bp.customList([(lambda x: x.uint32, 'time'),
                   (lambda x: x.uint32, 'stuntScore')],
                  'checkpoints')


def Chunk00C(bp):
    bp.uint32('u1')


def Chunk00E(bp):
    bp.lookbackString('uid')


def Chunk00F(bp):
    bp.string('ghostLogin')


def Chunk010(bp):
    bp.lookbackString('u1')


def Chunk012(bp):
    bp.uint32('u1')
    bp.bytes(16, name='u2')


def Chunk013(bp):
    bp.uint32('u1')
    bp.uint32('u2')


def Chunk014(bp):
    bp.uint32('u1')


def Chunk015(bp):
    bp.lookbackString('playerMobilId')


def Chunk017(bp):
    numSkins = bp.uint32('numSkins')
    for i in range(numSkins):
        bp.fileRef(f'skinPackDescs {i}')
    bp.string('ghostNickname')
    bp.string('ghostAvatarName')


def Chunk018(bp):
    bp.lookbackString('id')
    bp.lookbackString('collection')
    bp.lookbackString('author')


def Chunk019(bp):
    eventsDuration = bp.uint32('eventsDuration')
    if eventsDuration == 0:
        return
    bp.uint32('u1')
    bp.customList([(lambda x: x.lookbackString, 'controlNames')],
                  'controlNameList')
    numControlEntries = bp.uint32('numControlEntries')
    bp.uint32('u2')
    bp.customArray(numControlEntries,
                   [(lambda x: x.uint32, 'time'),
                    (lambda x: x.byte, 'controlNameIndex'),
                    (lambda x: x.uint32, 'onOff')],
                   'controlEntries')
    bp.string('gameVersion')
    bp.uint32('exeChecksum')
    bp.uint32('osKind')
    bp.uint32('cpuKind')
    bp.string('raceSettingsXML')
    bp.uint32('u3')
