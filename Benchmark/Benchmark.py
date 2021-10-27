import random

from Parser import *
from ByteWriter import ByteWriter
from Headers import Block, Point
import BlockImporter
import dictdiffer
import Methods
import timeit
import os

NUMBER_OF_TEST = 10


def test_parse(directory, result):
    for f in os.listdir(directory):
        result["nb"] += 1

        try:
            g = Gbx(f"{os.getcwd()}\\{directory}\\{f}")
        except BaseException as e:
            print(f"ERROR : {e}")
            continue
        result["parsed"] += 1

        try:
            bw = ByteWriter()
            bw.valueHandler = g.root_parser.valueHandler
            bw.chunkOrder = g.root_parser.chunkOrder
            bw.nodeNames = g.root_parser.nodeNames
            bw.currentChunk = 0
            BlockImporter.chunkLink[0](bw)
        except BaseException as e:
            print(f"ERROR : {e}")
            continue
        result["written"] += 1


def time_parse(directory, r):
    d = {"nb": 0, "parsed": 0, "written": 0}
    d["time"] = timeit.timeit(lambda: test_parse(directory, d), number=NUMBER_OF_TEST)
    d["time"] /= NUMBER_OF_TEST
    d["nb"] //= NUMBER_OF_TEST
    d["parsed"] //= NUMBER_OF_TEST
    d["written"] //= NUMBER_OF_TEST
    r.write(f"{directory:10} {d['nb']:10} {d['parsed']:10} {d['written']:10}\t\t\t   {d['time']:.4f}\n")


r = open("results.txt", "w+")
r.write(f"Type           Number     Parsed    Written       Time in sec\n")
time_parse('Tracks', r)
time_parse('Replays', r)
r.close()









