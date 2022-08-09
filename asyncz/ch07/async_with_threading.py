import asyncio
import functools
import time
import requests
from concurrent.futures import ThreadPoolExecutor


def get_status_code(url: str):
    response = requests.get(url)
    return response.status_code


def multi_thread():
    start = time.time()

    with ThreadPoolExecutor() as pool:
        urls = ['https://www.google.com' for _ in range(10)]
        results = pool.map(get_status_code, urls)
        for r in results:
            print(r)

    end = time.time()
    print(f'finished requests in {end - start:.4f} second(s)')


async def async_threading():
    start = time.time()
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        urls = ['https://www.google.com' for _ in range(10)]
        tasks = [loop.run_in_executor(pool, functools.partial(get_status_code, url)) for url in urls]
        res = await asyncio.gather(*tasks)
        print(res)

    end = time.time()
    print(f'finished requests in {end - start:.4f} second(s)')


async def to_thread():
    start = time.time()
    urls = ['https://www.google.com' for _ in range(10)]
    tasks = [asyncio.to_thread(get_status_code, url) for url in urls]
    res = await asyncio.gather(*tasks)
    print(res)
    end = time.time()
    print(f'finished requests in {end - start:.4f} second(s)')


if __name__ == '__main__':

    multi_thread()
    asyncio.run(async_threading())
    asyncio.run(to_thread())
