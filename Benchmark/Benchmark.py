from typing import Union

from GbxWriter import GbxWriter
from GbxReader import GbxReader
from Gbx import Gbx

import logging
import Levenshtein
import timeit
import os

NUMBER_OF_TESTS = 2

logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s', datefmt='%H:%M:%S')


def try_parse_single(file: str) -> Union[Gbx, None]:
    try:
        reader = GbxReader(file)
    except BaseException:
        logging.error(f"Can't open file {file}")
        return None

    try:
        gbx = reader.readAll()
    except BaseException as e:
        return None

    return gbx


def try_write_single(gbx: Gbx) -> str:
    writer = GbxWriter()

    try:
        writer.writeAll(gbx)
    except BaseException as e:
        return ""

    return writer.data


def try_one_file(file: str) -> (float, float, float):
    time_parse = timeit.timeit(lambda: try_parse_single(file), number=NUMBER_OF_TESTS) * 1000 / NUMBER_OF_TESTS
    gbx = try_parse_single(file)
    if gbx is None:
        logging.error(f"Error parsing the file {file}")
        return time_parse, -1, -1

    time_write = timeit.timeit(lambda: try_write_single(gbx), number=NUMBER_OF_TESTS) * 1000 / NUMBER_OF_TESTS
    data = try_write_single(gbx)
    if not data:
        logging.error(f"Error writing for the file {file}")
        return time_parse, time_write, -1

    gbx_copy = try_parse_single(data)
    if gbx_copy is None:
        logging.error(f"Error re-reading the file {file}")
        return time_parse, time_write, -1

    ratio = Levenshtein.ratio(gbx.raw_data, gbx_copy.raw_data)
    return time_parse, time_write, ratio


def try_one_folder(folder: str) -> (float, float, float):
    m_parse, m_write, m_ratio = 0, 0, 0
    n_parse, n_write, n_total = 0, 0, 0
    for f in os.listdir(folder):
        n_total += 1
        path = os.path.join(os.getcwd(), folder, f)
        time_parse, time_write, ratio = try_one_file(path)
        if time_parse != -1:
            n_parse += 1
            m_parse += time_parse
        if time_write != -1:
            n_write += 1
            m_write += time_write
        if ratio != -1:
            m_ratio += ratio
    return m_parse / n_parse, m_write / n_write, m_ratio / n_total


def try_all_folders():
    r = open("results.txt", 'w')
    r.write(f"{'Type':<10} {'Average parsing time (ms)':^30} {'Average writing time (ms)':^30} {'Resemblance':^20}\n")
    r.close()
    for folder in os.listdir('SampleGbxFiles'):
        m_parse, m_write, m_ratio = try_one_folder(f'SampleGbxFiles/{folder}')
        r = open("results.txt", 'a')
        r.write(f"{folder:<10} {m_parse:^30.2f} {m_write:^30.2f} {f'{100*m_ratio:.3f}%':^20} \n")
        r.close()


try_all_folders()
