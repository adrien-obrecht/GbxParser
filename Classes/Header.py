from Lzo.Lzo import LZO
import logging
from GbxReader import GbxReader
from GbxWriter import GbxWriter
from GameIDs import ChunkId, NodeId
from Gbx import Gbx
from Containers import Node, Chunk


def readHead(bp: GbxReader) -> Gbx:
    g = Gbx()
    magic = bp.bytes(3, name='magic')

    if magic.decode('utf-8') != 'GBX':
        logging.warning("Not a Gbx file!")
        return g
    version = bp.int16('version')
    compression = bp.bytes(3, name='u1')
    if version >= 4:
        bp.byte('u2')

    if version >= 3:
        g.id = bp.nodeId('nodeId')

    if version >= 6:
        g = readUserData(bp, g)

    num_nodes = bp.uint32('numNodes')

    num_external_nodes = bp.uint32('numExternalNodes')
    if num_external_nodes > 0:
        logging.warning(f"Num external node is {num_external_nodes}! ")

    data_size = bp.uint32('dataSize')
    comp_data_size = bp.uint32('compDataSize')
    comp_data = bp.bytes(comp_data_size, name='compData')

    if comp_data_size <= 0:
        return g

    # bp.freezeCurrentChunk()
    bp.resetLookbackState()
    # former_value_handler = bp.value_handler
    # bp.value_handler = Node()
    # bp.value_handler.id = NodeId.Body

    bp.data = LZO().decompress(comp_data, data_size)
    bp.pos = 0
    node = bp.node()
    node.id = NodeId.Body
    # value_handler = bp.value_handler
    # bp.value_handler = former_value_handler
    # bp.value_handler['Body'] = value_handler
    g.node_list = [node]

    # bp.unfreezeCurrentChunk()
    # bp.storeCurrentChunk(0)
    return g


def readUserData(bp, g):
    entries = {}
    user_data_size = bp.uint32('userDataSize')
    if user_data_size:
        num_chunks = bp.uint32('numChunks')
        g.header_chunk_list = []
        for i in range(num_chunks):
            cid = bp.chunkId(f'{i} chunkId')
            size = bp.uint32(f'{i} size')
            bp.current_chunk[f'{i} size'] %= 2 ** 31  # Erase the "heavy chunk" marker
            entries[cid] = size

        cV = bp.current_chunk
        import BlockImporter as bi
        for cid, size in entries.items():
            bp.current_chunk = Chunk()
            bp.current_chunk.id = cid
            bp.resetLookbackState()
            if cid.value in bi.chunkLink:
                logging.info(f"Reading chunk {cid}")
                bi.chunkLink[cid.value](bp)
                # bp.chunk_order.append(cid)
                g.header_chunk_list.append(bp.current_chunk)
                # bp.storeCurrentChunk(cid)
            else:
                logging.warning(f"Skiping chunk {cid}")
                bp.skip(size)

        bp.current_chunk = cV
    return g


def writeHead(bp):
    bp.bytes(3, name='magic')

    version = bp.int16('version')
    bp.bytes(3, name='u1')
    if version >= 4:
        bp.byte('u2')

    if version >= 3:
        bp.chunkId('chunkId')

    if version >= 6:
        writeUserData(bp)

    bp.uint32('numNodes')

    num_external_nodes = bp.uint32('numExternalNodes')
    if num_external_nodes > 0:
        logging.info(f"Num external node is {num_external_nodes}0! ")

    if not bp.chunk_order:
        return

    bp_ = GbxWriter()
    bp_.chunk_order = bp.chunk_order
    bp_.value_handler = bp.value_handler
    bp_.node_index = bp.node_index
    bp_.node()

    data = bytes(bp_.data)
    compData = LZO().compress(bytes(data))
    bp.uint32(len(data), is_ref=False)
    bp.uint32(len(compData), is_ref=False)
    bp.bytes(0, compData, is_ref=False)


def writeUserData(bp):
    try:
        num_chunks = bp.uint32('numChunks')
    except KeyError:
        bp.uint32(0, is_ref=False)
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
    chunk_datas = []
    import BlockImporter as bi
    for _ in range(num_chunks):
        bp_.current_chunk = bp_.chunk_order[0]
        bp_.chunk_order = bp_.chunk_order[1:]
        logging.info(f"Writing chunk {bp_.current_chunk}")
        bi.chunkLink[bp_.current_chunk.value](bp_)
        chunk_datas += [bp_.data]
        bp_.data = bytearray()

    bp_.current_chunk = 0

    for i in range(num_chunks):
        bp_.chunkId(f'{i} chunkId')
        if len(bytes(chunk_datas[i])) < 17000:
            bp_.uint32(len(bytes(chunk_datas[i])), is_ref=False)
        else:
            bp_.uint32(len(bytes(chunk_datas[i])) + 2 ** 31, is_ref=False)

    for i in range(num_chunks):
        bp_.bytes(0, chunk_datas[i], is_ref=False)

    data = bytes(bp_.data)
    bp.uint32(len(data) + 4, is_ref=False)
    bp.uint32('numChunks')
    bp.bytes(0, data, is_ref=False)
    bp.chunk_order = bp_.chunk_order
