import logging
import copy
from concurrent.futures import ProcessPoolExecutor
import asyncio
import functools
import time
from typing import Dict, List
from multiprocessing import Value


logging.basicConfig(level=logging.INFO, format='[PID: %(process)d] %(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger()


map_progress: Value


def init(progress: Value):
    global map_progress
    map_progress = progress


def map_freq(text: str) -> Dict[str, int]:
    global map_progress
    logger.debug(f"Mapper with {text}.")
    words = text.split(" ")
    freqs = {}
    for w in words:
        if w in freqs:
            freqs[w] += 1
        else:
            freqs[w] = 1

    with map_progress.get_lock():
        map_progress.value += 1

    return freqs


async def progress_reporter(total_partitions: int):
    while map_progress.value < total_partitions:
        logger.info(f"Finished {map_progress.value}/{total_partitions} map operations")
        await asyncio.sleep(1)


def merge_dict(d1: Dict[str, int], d2: Dict[str, int])-> Dict[str, int]:
    merged = d1
    for key in d2:
        if key in merged:
            merged[key] = merged[key] + d2[key]
        else:
            merged[key] = d2[key]

    return merged


def partition(data: List, chunk_size: int) -> List:
    for i in range(0, len(data), chunk_size):
        yield data[i: i+chunk_size]


def reduce_func(d, c):
    logger.debug(f"Reducer with function {d}, data {c}")
    return functools.reduce(d, c)


async def reduce(loop, pool, counters, chunk_size) -> Dict[str, int]:
    logger.info(f"Reducer with {chunk_size = }")
    chunks: List[List[Dict[str, int]]] = list(partition(counters, chunk_size))
    reducers = []
    while len(chunks[0]) > 1:
        for chunk in chunks:
            reducer = functools.partial(reduce_func, merge_dict, chunk)
            reducers.append(loop.run_in_executor(pool, reducer))

        reducer_chunks: List = await asyncio.gather(*reducers)

        chunks = list(partition(reducer_chunks, chunk_size))
        reducers.clear()

    return chunks[0][0]


async def main(partition_size: int, problem_size: int = 10, workers: int=1):
    x = [
        "I know what I know",
        "I know that I know",
        "I don't know much",
        "They don't know much"
    ]
    contents = []
    [contents.extend(copy.deepcopy(x)) for i in range(problem_size)]

    global map_progress
    loop = asyncio.get_running_loop()
    tasks = []
    map_progress = Value('i', 0)

    with ProcessPoolExecutor(initializer=init, initargs=(map_progress, ), max_workers=workers) as pool:
        total_partitions = len(contents) // partition_size
        reporter = asyncio.create_task(progress_reporter(total_partitions))
        for chunk in partition(contents, partition_size):
            for c in chunk:
                tasks.append(loop.run_in_executor(pool, functools.partial(map_freq, c)))

        start = time.time()
        logger.info(f"Task number: {len(tasks)}")
        intermediate = await asyncio.gather(*tasks)
        await reporter
        logger.info(f"Map finished using {time.time() - start} sec")
        final_result = await reduce(loop, pool, intermediate, partition_size)
        end = time.time()
        logger.info(f"Reduce finished... {end - start}: {final_result} ")


if __name__ == '__main__':

    lines = ["I know what I know",
             "I know that I know",
             "I don't know much",
             "They don't know much"]

    # mapped = [map_freq(text) for text in lines]
    # for res in mapped:
    #     print(res)
    #
    # merged = functools.reduce(merge_dict, mapped)
    # print(f"merged: {merged}")

    size = 50000
    asyncio.run(main(100, problem_size=size, workers=10))
