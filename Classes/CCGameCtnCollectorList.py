"""CCGameCtnCollectorList 0301B"""


def Chunk000(bp):
    archiveCount = bp.uint32('archiveCount')
    for _ in range(archiveCount):
        bp.lookbackString('blockName')
        bp.lookbackString('collection')
        bp.lookbackString('author')
        bp.uint32('numPieces')
