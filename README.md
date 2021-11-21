# GbxParser

Python Library to interact with the *.Gbx* files from the game Trackmania. 
It handles reading and writing any .Gbx files.

It converts a file to a Gbx object where you can easily access data and modify it. Then you can save the data to a new .Gbx file and use it inside the game.

Supported Games:
- TMNF only for the moment

Supported file types:
- Challenge (read and write)
- Replay (read and write)
- Clip (read and write)

For a better understanding of the library, see the exemples that are provided

**Future plans**
 - Handle parsing of the ghost replay in the CGameGhost chunk
 - Parse map data from CGameCtnReplayRecord
 - Support reading and writing for all files that TMNF can create
 - Create a documentation
 - Release 1.0, create a pip package
 - Support reading and writing for all files that TMN can create