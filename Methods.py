from Headers import Block


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
    for i in range(vH['numBlocks']):
        b = Block()
        b.name = vH[f'blockName {i}']
        b.rotation = vH[f'rotation {i}']
        b.flags = vH[f'flags {i}']
        b.position = [vH[f'posX {i}'], vH[f'posY {i}'], vH[f'posZ {i}']]
        blockList.append(b)
    return blockList


def erasePassword(bw):
    bw.valueHandler[50606121]['CRC32'] = 1169808926
    bw.valueHandler[50606121]['passwordHash'] = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
