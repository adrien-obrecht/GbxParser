"""CGameCtnGhost"""


def Chunk005(bp):
    raceTime = bp.uint32()


def Chunk008(bp):
    numRespawns = bp.uint32()


def Chunk009(bp):
    lightTrailColor = bp.color()


def Chunk00A(bp):
    stuntsScore = bp.uint32()


def Chunk00B(bp):
    numCheckpoints = bp.uint32()
    for _ in range(numCheckpoints):
        time = bp.uint32()
        stuntsScore = bp.uint32()


def Chunk00C(bp):
    bp.uint32()


def Chunk00E(bp):
    uid = bp.lookbackString()


def Chunk00F(bp):
    ghostLogin = bp.string()


def Chunk010(bp):
    bp.lookbackString()


def Chunk012(bp):
    bp.uint32()
    bp.skip(16)


def Chunk013(bp):
    bp.uint32()
    bp.uint32()


def Chunk014(bp):
    bp.uint32()


def Chunk015(bp):
    playerMobilId = bp.lookbackString()


def Chunk017(bp):
    skinPackDescs = bp.array('fileRef')
    ghostNickname = bp.string()
    ghostAvatarName = bp.string()


def Chunk018(bp):
    id = bp.lookbackString()
    collection = bp.lookbackString()
    author = bp.lookbackString()


def Chunk019(bp):
    eventsDuration = bp.uint32()
    if eventsDuration == 0:
        return
    bp.uint32()
    controlNames = bp.array('lookbackString')

    numControlEntries = bp.uint32()
    bp.uint32()
    for _ in range(numControlEntries):
        time = bp.uint32()
        controlNameIndex = bp.byte()
        onOff = bp.uint32()

    gameVersion = bp.string()
    exeChecksum = bp.uint32()
    osKind = bp.uint32()
    cpuKind = bp.uint32()
    raceSettingsXML = bp.string()
    bp.uint32()

