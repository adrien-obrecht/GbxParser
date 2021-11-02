from Parser import *
from GbxWriter import GbxWriter
import BlockImporter
import logging
import timeit
import os

NUMBER_OF_TEST = 10

logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)


def test_parse(directory, result):
    for f in os.listdir(directory):
        result["nb"] += 1

        try:
            t = timeit.timeit(lambda: Gbx(f"{os.getcwd()}\\{directory}\\{f}"), number=NUMBER_OF_TEST) * 1000
        except BaseException as e:
            logging.error(e)
            continue
        result["parsed"] += 1
        result["time_parse"] = t
        g = Gbx(f"{os.getcwd()}\\{directory}\\{f}")
        g.parse_all()
        try:
            def f(g):
                bw = GbxWriter()
                bw.value_handler = g.root_parser.value_handler
                bw.chunk_order = g.root_parser.chunk_order
                bw.node_names = g.root_parser.node_names
                bw.current_chunk = 0
                BlockImporter.chunkLink[0](bw)
            t = timeit.timeit(lambda: f(g), number=NUMBER_OF_TEST) * 1000
        except BaseException as e:
            logging.error(e)
            continue
        result["written"] += 1
        result["time_write"] = t
    return result


def time_parse(directory, r):
    d = {"nb": 0, "parsed": 0, "written": 0, "discovered": 0, "time_parse": 0, "time_write": 0, "time_discovery": 0}
    d = test_parse(directory, d)
    d["time_parse"] /= NUMBER_OF_TEST
    d["time_write"] /= NUMBER_OF_TEST
    d['parsed'] /= d['nb'] / 100
    d['written'] /= d['nb'] / 100
    r.write(f"{directory:10} {d['nb']:10}\t\t{d['parsed']:.1f}%\t{d['time_parse']:.2f}\t\t{d['written']:.1f}%\t{d['time_write']:.2f}\n")


r = open("results.txt", "w+")
r.write(f"Type           Number       Parsed  (ms)       Written  (ms)\n")
time_parse('Tracks', r)
time_parse('Replays', r)
r.close()
