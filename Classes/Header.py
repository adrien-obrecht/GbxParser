import lzo
from GbxReader import GbxReader
from GbxWriter import GbxWriter


def readHead(bp):
    magic = bp.read(3, name='magic')

    if magic.decode('utf-8') != 'GBX':
        return "Not a Gbx file!"
    version = bp.int16('version')
    bp.read(3, name='u1')
    if version >= 4:
        bp.byte('u2')

    if version >= 3:
        bp.uint32('chunkId')

    if version >= 6:
        _read_user_data(bp)

    bp.uint32('numNodes')

    numExternalNodes = bp.uint32('numExternalNodes')
    if numExternalNodes > 0:
        print(f"Num external node is {numExternalNodes}! ")

    dataSize = bp.uint32('dataSize')
    compDataSize = bp.uint32('compDataSize')
    compData = bp.read(compDataSize, name='compData')

    if compDataSize > 0:
        data = bytearray(lzo.decompress(compData, False, dataSize))
    else:
        bp.valueHandler[0] = bp.chunkValue
        return bytearray()

    bp_ = GbxReader(data)
    bp_.valueHandler = bp.valueHandler
    bp_.chunkOrder = bp.chunkOrder
    bp_.nodeNames = bp.nodeNames
    cV = bp.chunkValue
    bp = bp_
    bp.readNode()
    bp.valueHandler[0] = cV
    return data


def _read_user_data(bp):
    entries = {}
    user_data_size = bp.uint32('userDataSize')
    if user_data_size:
        num_chunks = bp.uint32('numChunks')
        for i in range(num_chunks):
            cid = bp.uint32(f'{i} chunkId')
            size = bp.uint32(f'{i} size')
            bp.chunkValue[f'{i} size'] %= 2**31  # Erase the "heavy chunk" marker
            entries[cid] = size

        cV = bp.chunkValue
        import BlockImporter as bi
        for cid, size in entries.items():
            bp.chunkValue = {}
            if cid in bi.chunkLink:
                print(f"Reading chunk {hex(cid)}")
                bi.chunkLink[cid](bp)
                bp.chunkOrder.append(cid)
                bp.valueHandler[cid] = bp.chunkValue
            else:
                print(f"Skiping chunk {hex(cid)}")
                bp.skip(size)

        bp.chunkValue = cV


def writeHead(bp):
    bp.read(3, name='magic')

    version = bp.int16('version')
    bp.read(3, name='u1')
    if version >= 4:
        bp.byte('u2')

    if version >= 3:
        bp.uint32('chunkId')

    if version >= 6:
        _write_user_data(bp)

    bp.uint32('numNodes')

    numExternalNodes = bp.uint32('numExternalNodes')
    if numExternalNodes > 0:
        print(f"Num external node is {numExternalNodes}0! ")

    if not bp.chunkOrder:
        return

    bp_ = GbxWriter()
    bp_.chunkOrder = bp.chunkOrder
    bp_.valueHandler = bp.valueHandler
    bp_.nodeNames = bp.nodeNames
    bp_.nodeIndex = bp.nodeIndex
    bp_.readNode()

    data = bytes(bp_.data)
    compData = lzo.compress(bytes(data), 0, False)
    bp.uint32(len(data), isRef=False)
    bp.uint32(len(compData), isRef=False)
    bp.read(0, compData, isRef=False)


def _write_user_data(bp):
    try:
        num_chunks = bp.uint32('numChunks')
    except KeyError:
        bp.uint32(0, isRef=False)
        bp.chunkOrder = bp.chunkOrder[1:]
        return

    bp.data = bp.data[:-4]

    bp_ = GbxWriter()
    bp_.chunkOrder = bp.chunkOrder[1:]
    bp_.valueHandler = bp.valueHandler
    bp_.nodeIndex = bp.nodeIndex
    bp_.storedStrings = bp.storedStrings
    bp_.nodeNames = bp.nodeNames
    bp_.currentChunk = 0
    bp_.data = bytearray()
    chunkDatas = []
    import BlockImporter as bi
    for _ in range(num_chunks):
        bp_.currentChunk = bp_.chunkOrder[0]
        bp_.chunkOrder = bp_.chunkOrder[1:]
        print(f"Writing chunk {hex(bp_.currentChunk)}")
        bi.chunkLink[bp_.currentChunk](bp_)
        chunkDatas += [bp_.data]
        bp_.data = bytearray()

    bp_.currentChunk = 0

    for i in range(num_chunks):
        bp_.uint32(f'{i} chunkId')
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
    bp.chunkOrder = bp_.chunkOrder
