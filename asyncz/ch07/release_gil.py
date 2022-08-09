import functools
import hashlib
import os
import string
import time
import random
import asyncio
from concurrent.futures import ThreadPoolExecutor

from asyncz.util import async_timed


def random_password(length: int) -> bytes:
    ascii_lowercase = string.ascii_lowercase.encode()
    return b"".join(bytes(random.choice(ascii_lowercase)) for _ in range(length))


def hash(password: bytes) -> str:
    salt = os.urandom(16)
    return str(hashlib.scrypt(password, salt=salt, n=2048, p=1, r=8))


def single_thread(passwords):
    start = time.time()

    for password in passwords:
        hash(password)

    end = time.time()
    print(f"Finished in {end - start} seconds.")


@async_timed()
async def main(passwords):
    loop = asyncio.get_event_loop()
    tasks = []

    with ThreadPoolExecutor() as pool:
        for password in passwords:
            tasks.append(loop.run_in_executor(pool, functools.partial(hash, password)))

        await asyncio.gather(*tasks)


if __name__ == '__main__':

    passwords = [random_password(10) for _ in range(10_000)]

    # single_thread(passwords)
    asyncio.run(main(passwords))
