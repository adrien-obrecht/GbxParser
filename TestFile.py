import random

from Parser import *
from ByteWriter import ByteWriter
from Headers import Block
import BlockImporter
import StadiumBlocks
import dictdiffer
import Methods


g = Gbx("C:\\Users\\User\\Documents\\TmForever\\Tracks\\Challenges\\Map.Challenge.Gbx")


bw = ByteWriter()

bw.valueHandler = g.root_parser.valueHandler


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

# Methods.erasePassword(bw)

# Methods.pushBlockList(bw, blocks)


bw.currentChunk = 0
BlockImporter.chunkLink[0](bw)

g_ = Gbx(bw.data)

f = open("C:\\Users\\User\\Documents\\TmForever\\Tracks\\Challenges\\My CHallenges\\test.Challenge.Gbx", "wb+")
f.write(bytes(bw.data))
f.close()

print(bw.valueHandler)
print(g_.root_parser.valueHandler)

for diff in list(dictdiffer.diff(bw.valueHandler, g_.root_parser.valueHandler)):
    if len(str(diff[2][0])) < 111500:
        print(diff[:2])
        print(diff[2][0])
        print(diff[2][1])

print(hex(50823169))