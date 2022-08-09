import time
import asyncio
from asyncio.events import AbstractEventLoop
from functools import partial
from typing import List
from multiprocessing import Process, Pool
from concurrent.futures import ProcessPoolExecutor


def count(to: int) -> int:
    start = time.time()
    counter = 0
    for i in range(to):
        counter += 1

    end = time.time()

    print(f"Finished counting to {to} in {end-start} seconds")
    return counter


def hi(x):
    print(f"Hi {x}!")


def raw_process():
    start = time.time()
    p1 = Process(target=count, args=(1_000_000_0, ))
    p2 = Process(target=count, args=(3_000_000_0, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end = time.time()
    print(f"Computed in {end-start} seconds")


def pool_executors():
    with ProcessPoolExecutor() as pool:
        numbers = [1, 3, 5, 22, 100000000]
        for result in pool.map(count, numbers):
            print(result)


async def async_multi_processing():
    with ProcessPoolExecutor() as pool:
        loop: AbstractEventLoop = asyncio.get_event_loop()
        nums = [1, 3, 5, 22, 100000000]
        calls: List[partial[int]] = [partial(count, num) for num in nums]
        call_coros = []

        for call in calls:
            call_coros.append(loop.run_in_executor(pool, call))

        res = await asyncio.gather(*call_coros)

        for r in res:
            print(r)


if __name__ == '__main__':

    with Pool() as pool:
        h1 = pool.apply(hi, args=("Z", ))
        h2 = pool.apply(hi, args=("W", ))

    # pool_executors()

    asyncio.run(async_multi_processing())