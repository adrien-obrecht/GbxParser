from GbxReader import GbxReader
from GbxWriter import GbxWriter
import BlockImporter


NAME = "test.Clip"
PATH = "C:\\Users\\User\\Documents\\TrackMania\\Tracks\\Replays\\CreatedGhosts"

# Create an object that parses the given file
reader = GbxReader(f"{PATH}\\{NAME}.Gbx")
reader.parseAll()

# We can now modify data inside g (mostly the value handler)
# See Methods for more examples of how to properly handle it

# Create an object to write data to a file
writer = GbxWriter()
# initalise data with what g parsed
writer.value_handler = reader.value_handler
writer.chunk_order = reader.chunk_order
writer.current_chunk = 0

# Call the header function on the writer, which will try to write all the data in order
BlockImporter.chunkLink[0](writer)

# Save data to file
f = open(f"{PATH}\\Folder\\Copy_{NAME}.Gbx", "wb+")
f.write(bytes(writer.data))
f.close()
