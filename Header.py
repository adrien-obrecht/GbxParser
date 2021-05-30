import time

import lzo
from ByteReader import ByteReader
from ByteWriter import ByteWriter
import BlockImporter as bi


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
        print("Num external node is not 0! ")

    dataSize = bp.uint32('dataSize')
    compDataSize = bp.uint32('compDataSize')
    compData = bp.read(compDataSize, name='compData')
    data = bytearray(lzo.decompress(compData, False, dataSize))

    bp_ = ByteReader(data)
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
    num_chunks = bp.uint32('numChunks')
    for i in range(num_chunks):
        cid = bp.uint32(f'{i} chunkId')
        size = bp.uint32(f'{i} size')
        entries[cid] = size

    cV = bp.chunkValue
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
        print("Num external node is not 0! ")

    bp_ = ByteWriter()
    bp_.chunkOrder = bp.chunkOrder
    bp_.valueHandler = bp.valueHandler
    bp_.nodeNames = bp.nodeNames
    bp_.nodeIndex = bp.nodeIndex
    bp_.readNode()

    data = bytes(bp_.data)
    compData = lzo.compress(bytes(data), 1, False)
    bp.uint32(len(data), isRef=False)
    bp.uint32(len(compData), isRef=False)
    bp.read(0, compData, isRef=False)


def _write_user_data(bp):
    # user_data_size = bp.uint32('userDataSize')
    bp_ = ByteWriter()
    bp_.chunkOrder = bp.chunkOrder[1:]
    bp_.valueHandler = bp.valueHandler
    bp_.nodeIndex = bp.nodeIndex
    bp_.storedStrings = bp.storedStrings
    bp_.nodeNames = bp.nodeNames
    bp_.currentChunk = 0

    num_chunks = bp_.uint32('numChunks')
    bp_.data = bytearray()
    chunkDatas = []
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
        if len(bytes(chunkDatas[i])) < 200:
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
