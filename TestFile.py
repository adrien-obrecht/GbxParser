import random

from Parser import *
from ByteWriter import ByteWriter
from Headers import Block
import BlockImporter
import StadiumBlocks
import Methods


g = Gbx("C:\\Users\\User\\Documents\\TmForever\\Tracks\\_Somewhere_I_belong.Challenge.Gbx")


bw = ByteWriter()

bw.valueHandler = g.root_parser.valueHandler
print(bw.valueHandler)


bw.chunkOrder = g.root_parser.chunkOrder
bw.nodeNames = g.root_parser.nodeNames

blocks = []
posList = set()
for i in range(300):
    b = Block()
    b.position = [random.randint(5, 25), random.randint(2, 12), random.randint(5, 25)]
    b.rotation = random.randint(0, 3)
    b.flags = 0
    b.name = StadiumBlocks.STADIUM_BLOCKS[random.randint(0, len(StadiumBlocks.STADIUM_BLOCKS)-1)]
    if str(b.position) not in posList:
        posList.add(str(b.position))
        blocks.append(b)

Methods.erasePassword(bw)

# Methods.pushBlockList(bw, blocks)


bw.currentChunk = 0
BlockImporter.chunkLink[0](bw)

# g_ = Gbx(bw.data)

f = open("C:\\Users\\User\\Documents\\TmForever\\Tracks\\Challenges\\My CHallenges\\test.Challenge.Gbx", "wb+")
f.write(bytes(bw.data))
f.close()

print(bw.valueHandler)

