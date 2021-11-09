from Lzo.Lzo import LZO
import logging
from GbxReader import GbxReader
from GbxWriter import GbxWriter
from Containers import Node


def readHead(bp: GbxReader):
    magic = bp.read(3, name='magic')

    if magic.decode('utf-8') != 'GBX':
        logging.warning("Not a Gbx file!")
        return
    version = bp.int16('version')
    bp.read(3, name='u1')
    if version >= 4:
        bp.byte('u2')

    if version >= 3:
        chunkId = bp.chunkId('chunkId')
        bp.chunk_value.id = chunkId

    if version >= 6:
        readUserData(bp)

    bp.uint32('numNodes')

    numExternalNodes = bp.uint32('numExternalNodes')
    if numExternalNodes > 0:
        logging.info(f"Num external node is {numExternalNodes}! ")

    dataSize = bp.uint32('dataSize')
    compDataSize = bp.uint32('compDataSize')
    compData = bp.read(compDataSize, name='compData')

    if compDataSize <= 0:
        bp.value_handler[0] = bp.chunk_value
        return

    bp.freezeCurrentChunk()
    bp.resetLookbackState()

    bp.data = LZO().decompress(compData, dataSize)
    bp.pos = 0
    bp.readNode()

    bp.unfreezeCurrentChunk()
    bp.storeCurrentChunk(0)
    return


def readUserData(bp):
    entries = {}
    user_data_size = bp.uint32('userDataSize')
    if user_data_size:
        num_chunks = bp.uint32('numChunks')
        for i in range(num_chunks):
            cid = bp.chunkId(f'{i} chunkId')
            size = bp.uint32(f'{i} size')
            bp.chunk_value[f'{i} size'] %= 2 ** 31  # Erase the "heavy chunk" marker
            entries[cid] = size

        cV = bp.chunk_value
        import BlockImporter as bi
        for cid, size in entries.items():
            bp.chunk_value = Node()
            bp.resetLookbackState()
            if cid.value in bi.chunkLink:
                logging.info(f"Reading chunk {cid}")
                bi.chunkLink[cid.value](bp)
                bp.chunk_order.append(cid)
                bp.storeCurrentChunk(cid)
            else:
                logging.info(f"Skiping chunk {cid}")
                bp.skip(size)

        bp.chunk_value = cV


def writeHead(bp):
    bp.read(3, name='magic')

    version = bp.int16('version')
    bp.read(3, name='u1')
    if version >= 4:
        bp.byte('u2')

    if version >= 3:
        bp.chunkId('chunkId')

    if version >= 6:
        writeUserData(bp)

    bp.uint32('numNodes')

    numExternalNodes = bp.uint32('numExternalNodes')
    if numExternalNodes > 0:
        logging.info(f"Num external node is {numExternalNodes}0! ")

    if not bp.chunk_order:
        return

    bp_ = GbxWriter()
    bp_.chunk_order = bp.chunk_order
    bp_.value_handler = bp.value_handler
    bp_.node_index = bp.node_index
    bp_.readNode()

    data = bytes(bp_.data)
    compData = LZO().compress(bytes(data))
    bp.uint32(len(data), isRef=False)
    bp.uint32(len(compData), isRef=False)
    bp.read(0, compData, isRef=False)


def writeUserData(bp):
    try:
        num_chunks = bp.uint32('numChunks')
    except KeyError:
        bp.uint32(0, isRef=False)
        bp.chunk_order = bp.chunk_order[1:]
        return

    bp.data = bp.data[:-4]

    bp_ = GbxWriter()
    bp_.chunk_order = bp.chunk_order[1:]
    bp_.value_handler = bp.value_handler
    bp_.node_index = bp.node_index
    bp_.stored_strings = bp.stored_strings
    bp_.current_chunk = 0
    bp_.data = bytearray()
    chunkDatas = []
    import BlockImporter as bi
    for _ in range(num_chunks):
        bp_.current_chunk = bp_.chunk_order[0]
        bp_.chunk_order = bp_.chunk_order[1:]
        logging.info(f"Writing chunk {bp_.current_chunk}")
        bi.chunkLink[bp_.current_chunk.value](bp_)
        chunkDatas += [bp_.data]
        bp_.data = bytearray()

    bp_.current_chunk = 0

    for i in range(num_chunks):
        bp_.chunkId(f'{i} chunkId')
        if len(bytes(chunkDatas[i])) < 17000:
            bp_.uint32(len(bytes(chunkDatas[i])), isRef=False)
        else:
            bp_.uint32(len(bytes(chunkDatas[i]))+2**31, isRef=False)

    for i in range(num_chunks):
        bp_.read(0, chunkDatas[i], isRef=False)

    data = bytes(bp_.data)
    bp.uint32(len(data) + 4, isRef=False)
    bp.uint32('numChunks')
    bp.read(0, data, isRef=False)
    bp.chunk_order = bp_.chunk_order
