import time

from Parser import *
from Headers import Block
import DiscordDownloader
import os
from SpreadsheetModifier import writeRow
import Methods

DRAGABLE_LIST = ["StadiumPool", "StadiumDirt", "StadiumInflatableSupport"]
FAKE_BLOCKS = ["StadiumGrassClip", "StadiumInflatablePillar", "StadiumDirtClip"]


def read(link, NUM=2):
    g = Gbx(link)

    name = link.split('%')

    name[3] = name[3].replace("_", " ")
    name[3] = name[3].replace("§", ":")
    name[3] = name[3].replace("-", "/")

    EVALUATION = [name[1], name[2], name[3], 0]

    vH = g.root_parser.valueHandler
    blockList = Methods.getBlockList(g.root_parser)
    blockCounter = {}

    # Remove clips / zepelin base
    blockList = [block for block in blockList if block.name not in FAKE_BLOCKS]

    # Add dirt between barrers
    barrerList = [b for b in blockList if b.name == "StadiumDirtBorder"]
    dirtList = [b for b in blockList if b.name == "StadiumDirt"]
    for block in barrerList:
        neighboursXPlus = []
        neighboursXMinus = []
        neighboursZPlus = []
        neighboursZMinus = []
        pos = block.position
        for b in barrerList:
            if b.position[0] == pos[0] or b.position[2] == pos[2]:
                if b.position[0] > pos[0]:
                    neighboursXPlus.append(b)
                elif b.position[0] < pos[0]:
                    neighboursXMinus.append(b)
                elif b.position[2] > pos[2]:
                    neighboursZPlus.append(b)
                elif b.position[2] < pos[2]:
                    neighboursZMinus.append(b)

        if len(neighboursXPlus) == 1:
            b = neighboursXPlus[0]
            for i in range(pos[0] + 1, b.position[0]):
                newBlock = Block()
                newBlock.name = "StadiumDirt"
                newBlock.position = [i, pos[1], pos[2]]
                if newBlock not in dirtList:
                    dirtList.append(newBlock)

        if len(neighboursXMinus) == 1:
            b = neighboursXMinus[0]
            for i in range(b.position[0] + 1, pos[0]):
                newBlock = Block()
                newBlock.name = "StadiumDirt"
                newBlock.position = [i, pos[1], pos[2]]
                if newBlock not in dirtList:
                    dirtList.append(newBlock)

        if len(neighboursZPlus) == 1:
            b = neighboursZPlus[0]
            for i in range(pos[2] + 1, b.position[2]):
                newBlock = Block()
                newBlock.name = "StadiumDirt"
                newBlock.position = [pos[0], pos[1], i]
                if newBlock not in dirtList:
                    dirtList.append(newBlock)

        if len(neighboursZMinus) == 1:
            b = neighboursZMinus[0]
            for i in range(b.position[2] + 1, pos[2]):
                newBlock = Block()
                newBlock.name = "StadiumDirt"
                newBlock.position = [pos[0], pos[1], i]
                if newBlock not in dirtList:
                    dirtList.append(newBlock)

        for b in dirtList:
            if b not in blockList:
                blockList.append(b)

    # Merge terrain borders + count not dragable blocks
    for block in blockList:
        if "StadiumDirt" in block.name:
            block.name = "StadiumDirt"
        if "StadiumWater" in block.name:
            block.name = "StadiumPool"
        if block.name in blockCounter:
            blockCounter[block.name] += 1
        elif not isDragable(block):
            blockCounter[block.name] = 1

    mem = set()

    for block in blockList:
        if isDragable(block):
            mem.add((block.name, get_angle_pos(block, blockList), get_angle_neg(block, blockList)))

    dragCount = len(mem)
    mem = {el for el in mem if el[1] != el[2]}

    EVALUATION.append(
            f"{len([block for block in blockList if not isDragable(block)]) + dragCount} / {vH[50606082]['cost']}")
    if vH[50606082]['cost'] % (len([block for block in blockList if not isDragable(block)]) + dragCount) != 0:
        EVALUATION.append("False")
    else:
        EVALUATION.append("OK")

    drag = {}
    for el in mem:
        if el[0] not in drag:
            drag[el[0]] = 1
        else:
            drag[el[0]] += 1

    strEval = ""
    for key in drag.keys():
        strEval += f"{drag[key]} {key} \n"
    if not strEval:
        strEval = "0 \n"

    EVALUATION.append(strEval[:-2])

    errorBlocks = set()
    for key in blockCounter.keys():
        if blockCounter[key] > 2:
            errorBlocks.add((key, blockCounter[key]))

    for key in drag.keys():
        if drag[key] > 2:
            errorBlocks.add((key, drag[key]))

    strEval = ""
    for err in errorBlocks:
        strEval += f"{err[1]} {err[0]} \n"
    if not strEval:
        strEval = "None \n"
    EVALUATION.append(strEval[:-2])
    if not errorBlocks:
        EVALUATION.append("OK")
    else:
        EVALUATION.append("False")

    numCheckpoint = 0
    numBooster = 0
    for block in blockList:
        if "Checkpoint" in block.name:
            numCheckpoint += 1
        if "Turbo" in block.name:
            numBooster += 1
    EVALUATION.append(f'{numBooster} = {numCheckpoint}')
    if numBooster == numCheckpoint:
        EVALUATION.append("OK")
    else:
        EVALUATION.append("False")

    finishes = set()
    start = None
    for block in blockList:
        if "StartLine" in block.name:
            start = block
        if "Finish" in block.name:
            finishes.add(block)

    EVALUATION.append(len(finishes))

    if len(finishes) <= 1:
        EVALUATION.append("OK")
    else:
        EVALUATION.append("False")

    maxStartFinDistance = 0

    for fin in finishes:
        maxStartFinDistance = max(abs(fin.position[0] - start.position[0]), maxStartFinDistance)
        maxStartFinDistance = max(abs(fin.position[1] - start.position[1]), maxStartFinDistance)
        maxStartFinDistance = max(abs(fin.position[2] - start.position[2]), maxStartFinDistance)

    EVALUATION.append(maxStartFinDistance)

    if maxStartFinDistance <= 2:
        EVALUATION.append("OK")
    else:
        EVALUATION.append("False")

    EVALUATION[3] = f'{EVALUATION.count("OK")} / 5'

    writeRow(NUM, EVALUATION)


def isDragable(block):
    return block.name in DRAGABLE_LIST


def compute_x_drag(block, blockList):
    maxX = block.position[0]
    minX = maxX
    modif = -1
    while modif != 0:
        modif = 0
        for b in blockList:
            if b.position[0] + 1 == minX and b.position[1] == block.position[1] and b.position[2] == block.position[
                2] and b.name == block.name:
                minX -= 1
                modif += 1
            if b.position[0] - 1 == maxX and b.position[1] == block.position[1] and b.position[2] == block.position[
                2] and b.name == block.name:
                maxX += 1
                modif += 1
    return minX, maxX


def compute_y_drag(block, blockList):
    maxY = block.position[2]
    minY = maxY
    modif = -1
    while modif != 0:
        modif = 0
        for b in blockList:
            if b.position[0] == block.position[0] and b.position[1] == block.position[1] and b.position[
                2] + 1 == minY and b.name == block.name:
                minY -= 1
                modif += 1
            if b.position[0] == block.position[0] and b.position[1] == block.position[1] and b.position[
                2] - 1 == maxY and b.name == block.name:
                maxY += 1
                modif += 1
    return minY, maxY


def get_angle_pos(block, blockList):
    modif = -1
    posX = block.position[0]
    posY = block.position[1]
    posZ = block.position[2]
    name = block.name
    while modif != 0:
        modif = 0
        for b in blockList:
            if b.position == [posX + 1, posY, posZ] and b.name == name:
                posX += 1
                modif = 1
    modif = -1
    while modif != 0:
        modif = 0
        for b in blockList:
            if b.position == [posX, posY, posZ + 1] and b.name == name:
                posZ += 1
                modif = 1
    return posX, posZ


def get_angle_neg(block, blockList):
    modif = -1
    posX = block.position[0]
    posY = block.position[1]
    posZ = block.position[2]
    name = block.name
    while modif != 0:
        modif = 0
        for b in blockList:
            if b.position == [posX - 1, posY, posZ] and b.name == name:
                posX -= 1
                modif = 1
    modif = -1
    while modif != 0:
        modif = 0
        for b in blockList:
            if b.position == [posX, posY, posZ - 1] and b.name == name:
                posZ -= 1
                modif = 1
    return posX, posZ


PATH = "/EHEMC Tracks"

DiscordDownloader.run()

print("Starting map evaluation...")

i = 3
for path in os.listdir(PATH):
    try:
        read(PATH + "\\" + path, i)
    except Exception as e:
        name = path.split('%')

        name[3] = name[3].replace("_", " ")
        name[3] = name[3].replace("§", ":")
        name[3] = name[3].replace("-", "/")

        print(f"Caught an exception : {type(e).__name__} {e.args}")
        writeRow(i, name[1:4] + ["", "Failed to parse the replay!"] + [""] * 10)
    i += 1

dragStr = "Dragable blocks : "

for _block in DRAGABLE_LIST:
    dragStr += _block + " "

writeRow(1,
         ["Bot made by Adrien#1910", "", "", f"""Last update : {time.strftime('%m/%d %H:%M.%S')}""", "", "", dragStr])

print(f"Correctly evaluated {i - 3} maps!")

os._exit(0)
