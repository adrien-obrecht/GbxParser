from Parser import *
from GbxWriter import GbxWriter
import BlockImporter


NAME = "test.Clip"
PATH = "C:\\Users\\User\\Documents\\TrackMania\\Tracks\\Replays\\CreatedGhosts"

# Create an object that parses the given file
g = Gbx(f"{PATH}\\{NAME}.Gbx")
g.parse_all()

# We can now modify data inside g (mostly the value handler)
# See Methods for more examples of how to properly handle it

# Create an object to write data to a file
bw = GbxWriter()
# initalise data with what g parsed
bw.value_handler = g.root_parser.value_handler
bw.chunk_order = g.root_parser.chunk_order
bw.node_names = g.root_parser.node_names
bw.current_chunk = 0

# Call the header function on the writer, which will try to write all the data in order
BlockImporter.chunkLink[0](bw)

# Save data to file
f = open(f"{PATH}\\Folder\\Copy_{NAME}.Gbx", "wb+")
f.write(bytes(bw.data))
f.close()
