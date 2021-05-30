"""CGameGhost"""

import zlib
from ByteReader import ByteReader


def Chunk005(bp):
    uncompSize = bp.uint32('')
    compSize = bp.uint32()
    compData = bp.read(compSize)
    data = zlib.decompress(compData, 0, uncompSize)

    gr = ByteReader(data)
    classId = gr.uint32()
    bSkipList2 = gr.bool()
    gr.uint32()
    samplePeriod = gr.uint32()
    gr.uint32()

    sampleDataSize = gr.uint32()
    gr.skip(sampleDataSize)

    num_samples = gr.uint32()
    if num_samples > 0:
        firstSampleOffset = gr.uint32()
        if num_samples > 1:
            sizePerSample = gr.int32()
            if sizePerSample == -1:
                sampleSizes = []
                for _ in range(num_samples - 1):
                    sampleSizes.append(gr.uint32())

    if not bSkipList2:
        num = bp.uint32()
        sampleTimes = bp.array('uint32')
