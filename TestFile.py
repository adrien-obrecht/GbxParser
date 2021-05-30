import random

from Parser import *
from ByteWriter import ByteWriter
from Headers import Block
import BlockImporter
import StadiumBlocks


def getBlockList(bw):
    vH = bw.valueHandler[50606111]
    print(vH)
    blockList = []
    for i in range(vH['numBlocks']):
        b = Block()
        b.name = vH[f'blockName {i}']
        b.rotation = vH[f'rotation {i}']
        b.flags = vH[f'flags {i}']
        b.position = [vH[f'posX {i}'], vH[f'posY {i}'], vH[f'posZ {i}']]
        blockList.append(b)
    return blockList


def writeBlockList(bw, blockList):
    bw.valueHandler[50606111]['numBlocks'] = len(blockList)
    for i, block in enumerate(blockList):
        bw.valueHandler[50606111][f'posX {i}'] = block.position[0]
        bw.valueHandler[50606111][f'posY {i}'] = block.position[1]
        bw.valueHandler[50606111][f'posZ {i}'] = block.position[2]
        bw.valueHandler[50606111][f'blockName {i}'] = block.name
        bw.valueHandler[50606111][f'rotation {i}'] = block.rotation
        bw.valueHandler[50606111][f'flags {i}'] = block.flags


g = Gbx("C:\\Users\\User\\Documents\\TmForever\\Tracks\\Map.Challenge.Gbx")


bw = ByteWriter()

bw.valueHandler = g.root_parser.valueHandler
print(bw.valueHandler)


bw.chunkOrder = g.root_parser.chunkOrder
bw.nodeNames = g.root_parser.nodeNames

blocks = getBlockList(bw)
for i in range(10):
    b = Block()
    b.position = [random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)]
    b.rotation = random.randint(0, 4)
    b.flags = 0
    b.name = 'StadiumRoadMainStartLine'
    blocks.append(b)
writeBlockList(bw, blocks)
print(bw.valueHandler[50606111])
bw.currentChunk = 0
BlockImporter.chunkLink[0](bw)


g_ = Gbx(bw.data)

f = open("C:\\Users\\User\\Documents\\TmForever\\Tracks\\Challenges\\test.Challenge.Gbx", "wb+")
f.write(bytes(bw.data))
f.close()



