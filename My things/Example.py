import random

from Parser import *
from ByteWriter import ByteWriter
from Headers import Block, Point
import BlockImporter
import dictdiffer
import Methods

name = "test.Challenge"
# path = "C:\\Users\\User\\Documents\\TrackMania\\Tracks\\Replays\\CreatedGhosts"
path = "C:\\Users\\User\\Documents\\TrackMania\\Tracks\\Challenges\\My Challenges"
g = Gbx(f"{path}\\{name}.Gbx")

print(g.root_parser.valueHandler)

bw = ByteWriter()
bw.valueHandler = g.root_parser.valueHandler
bw.chunkOrder = g.root_parser.chunkOrder
bw.nodeNames = g.root_parser.nodeNames
bw.currentChunk = 0

# Methods.erasePassword(bw)

BlockImporter.chunkLink[0](bw)

import binascii
g.root_parser.data.seek(0)
print(binascii.hexlify(g.root_parser.data.read()))
print(binascii.hexlify(bw.data))

f = open(f"{path}\\Folder\\Copy_{name}.Gbx", "wb+")
f.write(bytes(bw.data))
f.close()

g_ = Gbx(f"{path}\\Folder\\Copy_{name}.Gbx")
print(g.root_parser.valueHandler)
print(g_.root_parser.valueHandler)

for diff in list(dictdiffer.diff(bw.valueHandler, g_.root_parser.valueHandler)):
    if len(str(diff[2][0])) < 1500:
        print(diff)



