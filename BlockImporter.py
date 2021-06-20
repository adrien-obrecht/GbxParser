import Class0301B
import Class0305B
import Class0303F
import Class03043
import Class03059
import Class03078
import Class03079
import Class0307A
import Class03082
import Class03084
import Class03092
import Class03093
import Class030A2
import Class030A5
import Class030A8
import Class030AB
import Class030E5
import Class07010
import Header

chunkLink = {0x00000000: Header.writeHead,

             0x0301B000: Class0301B.Chunk000,

             0x0305B001: Class0305B.Chunk001,
             0x0305B004: Class0305B.Chunk004,
             0x0305B008: Class0305B.Chunk008,

             0x0303F005: Class0303F.Chunk005,

             0x03043002: Class03043.Chunk002,
             0x03043003: Class03043.Chunk003,
             0x03043004: Class03043.Chunk004,
             0x03043005: Class03043.Chunk005,
             0x03043007: Class03043.Chunk007,
             0x0304300D: Class03043.Chunk00D,
             0x03043011: Class03043.Chunk011,
             0x03043017: Class03043.Chunk017,
             0x03043018: Class03043.Chunk018,
             0x03043019: Class03043.Chunk019,
             0x0304301C: Class03043.Chunk01C,
             0x0304301F: Class03043.Chunk01F,
             0x03043021: Class03043.Chunk021,
             0x03043022: Class03043.Chunk022,
             0x03043024: Class03043.Chunk024,
             0x03043025: Class03043.Chunk025,
             0x03043026: Class03043.Chunk026,
             0x03043028: Class03043.Chunk028,
             0x03043029: Class03043.Chunk029,
             0x0304302A: Class03043.Chunk02A,

             0x03059002: Class03059.Chunk002,

             0x03078001: Class03078.Chunk001,
             0x03078004: Class03078.Chunk004,

             0x03079004: Class03079.Chunk004,
             0x03079005: Class03079.Chunk005,
             0x03079007: Class03079.Chunk007,

             0x0307A003: Class0307A.Chunk003,

             0x03082000: Class03082.Chunk000,

             0x03084003: Class03084.Chunk003,

             0x03092005: Class03092.Chunk005,
             0x03092008: Class03092.Chunk008,
             0x03092009: Class03092.Chunk009,
             0x0309200A: Class03092.Chunk00A,
             0x0309200B: Class03092.Chunk00B,
             0x0309200C: Class03092.Chunk00C,
             0x0309200E: Class03092.Chunk00E,
             0x0309200F: Class03092.Chunk00F,
             0x03092010: Class03092.Chunk010,
             0x03092012: Class03092.Chunk012,
             0x03092013: Class03092.Chunk013,
             0x03092014: Class03092.Chunk014,
             0x03092015: Class03092.Chunk015,
             0x03092017: Class03092.Chunk017,
             0x03092018: Class03092.Chunk018,
             0x03092019: Class03092.Chunk019,

             0x03093000: Class03093.Chunk000,
             0x03093001: Class03093.Chunk001,
             0x03093002: Class03093.Chunk002,
             0x03093007: Class03093.Chunk007,
             0x03093014: Class03093.Chunk014,

             0x030A2005: Class030A2.Chunk005,

             0x030A5000: Class030A5.Chunk000,

             0x030A8001: Class030A8.Chunk001,
             0x030A8002: Class030A8.Chunk002,

             0x030AB000: Class030AB.Chunk000,

             0x030E5001: Class030E5.Chunk001,

             0x07010003: Class07010.Chunk003,
             0x07010005: Class07010.Chunk005}

skipableChunkList = {0x03043017,
                     0x03043018,
                     0x03043019,
                     0x0304301C,
                     0x03043029,
                     }