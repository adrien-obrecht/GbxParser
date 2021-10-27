from Parser import *
from ByteWriter import ByteWriter
import BlockImporter


NAME = "test.Clip"
PATH = "C:\\Users\\User\\Documents\\TrackMania\\Tracks\\Replays\\CreatedGhosts"

# Create an object that parses the given file
g = Gbx(f"{PATH}\\{NAME}.Gbx")

# We can now modify data inside g (mostly the value handler)
# See Methods for more examples of how to properly handle it

# Create an object to write data to a file
bw = ByteWriter()
# initalise data with what g parsed
bw.valueHandler = g.root_parser.valueHandler
bw.chunkOrder = g.root_parser.chunkOrder
bw.nodeNames = g.root_parser.nodeNames
bw.currentChunk = 0

# Call the header function on the writer, which will try to write all the data in order
BlockImporter.chunkLink[0](bw)

# Save data to file
f = open(f"{PATH}\\Folder\\Copy_{NAME}.Gbx", "wb+")
f.write(bytes(bw.data))
f.close()
