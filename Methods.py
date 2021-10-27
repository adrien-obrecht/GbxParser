import binascii

from Headers import Block, Point, Vector3


def pushBlockList(bw, blockList):
    bw.valueHandler[50606111]['numBlocks'] = len(blockList)
    for i, block in enumerate(blockList):
        bw.valueHandler[50606111][f'posX {i}'] = block.position[0]
        bw.valueHandler[50606111][f'posY {i}'] = block.position[1]
        bw.valueHandler[50606111][f'posZ {i}'] = block.position[2]
        bw.valueHandler[50606111][f'blockName {i}'] = block.name
        bw.valueHandler[50606111][f'rotation {i}'] = block.rotation
        bw.valueHandler[50606111][f'flags {i}'] = block.flags


def getBlockList(bw):
    vH = bw.valueHandler[50606111]
    blockList = []
    storedName = ""
    for i in range(vH['numBlocks']):
        b = Block()
        b.name = vH[f'blockName {i}']
        b.rotation = vH[f'rotation {i}']
        b.flags = vH[f'flags {i}']
        b.position = [vH[f'posX {i}'], vH[f'posY {i}'], vH[f'posZ {i}']]
        if b.name == "":
            b.name = storedName
        storedName = b.name
        blockList.append(b)
    return blockList


def erasePassword(bw):
    trackUID = bw.valueHandler[50606083]['trackUID']
    string = f"0x00000000000000000000000000000000???{trackUID}"

    bw.valueHandler[50606121]['CRC32'] = binascii.crc32(bytes(string, 'utf-8'))
    bw.valueHandler[50606121]['passwordHash'] = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'



def getTrianglesInfo(bw):
    vH = bw.valueHandler[50827269]['mediaTrack 0'][50823169]['mediaBlock 0'][50499585]
    numKeys = vH['numKeys']
    numPoints = vH['numPoints']
    numTriangles = vH['numTriangles']
    pointList = [Point() for _ in range(numPoints)]
    timeList = [0 for _ in range(numKeys)]
    triangleList = [(0, 1, 2) for _ in range(numTriangles)]
    for p in range(numPoints):
        point = pointList[p]
        point.opacity = vH[f'opacity {p}']
        point.color = vH[f'pointColor {p}']
    for i in range(numKeys):
        timeList[i] = vH[f'timeStamp {i}']
        for j in range(numPoints):
            point = pointList[j]
            point.positions.append(vH[f'pointPosition {i} {j}'])
    for i in range(numTriangles):
        triangleList[i] = (vH[f'vertex1 {i}'], vH[f'vertex2 {i}'], vH[f'vertex3 {i}'])
    return pointList, timeList, triangleList


def pushTriangleInfo(bw, pointList, timeList, triangleList):
    vH = {}
    vH['numKeys'] = len(timeList)
    vH['numPoints'] = len(pointList)
    vH['numTriangles'] = len(triangleList)

    for i, time in enumerate(timeList):
        vH[f'timeStamp {i}'] = time

    for i in range(len(timeList)):
        for j, point in enumerate(pointList):
            vH[f'pointPosition {i} {j}'] = point.positions[i]

    for i, point in enumerate(pointList):
        vH[f'pointColor {i}'] = point.color
        vH[f'opacity {i}'] = point.opacity

    for i, triangle in enumerate(triangleList):
        vH[f'vertex1 {i}'] = triangle[0]
        vH[f'vertex2 {i}'] = triangle[1]
        vH[f'vertex3 {i}'] = triangle[2]

    vH['u1'] = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    bw.valueHandler[50827269]['mediaTrack 0'][50823169]['mediaBlock 0'][50499585] = vH
