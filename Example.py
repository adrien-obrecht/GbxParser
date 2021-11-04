from GbxReader import GbxReader
from GbxWriter import GbxWriter


NAME = "test.Clip"
PATH = "C:\\Users\\User\\Documents\\TrackMania\\Tracks\\Replays\\CreatedGhosts"

# Create an object that parses the given file
reader = GbxReader(f"{PATH}\\{NAME}.Gbx")
reader.parseAll()

# We can now modify data inside reader (mostly the value handler)
# See Methods for more examples of how to properly handle it

# Create an object to write data to a file
writer = GbxWriter()
# initalise data with what the reader parsed
writer.value_handler = reader.value_handler
writer.chunk_order = reader.chunk_order

# Call the header function on the writer, which will try to write all the data in order
writer.writeAll()

# Save data to file
writer.saveToFile(f"{PATH}\\Folder\\Copy_{NAME}.Gbx")
