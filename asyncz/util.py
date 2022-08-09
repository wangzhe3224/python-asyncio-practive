from typing import Callable, Any
import time 
import functools
import asyncio

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger()


async def delay(delay_seconds: int) -> int:
    print(f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print(f'finished sleeping for {delay_seconds} second(s)') 
    
    return delay_seconds


def async_timed():

    def wrapper(func: Callable) -> Callable:

        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f"starting {func} with {args =} {kwargs = }")
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f"finished {func} in {total: .4f} seconds.")

        return wrapped
        
    return wrapper