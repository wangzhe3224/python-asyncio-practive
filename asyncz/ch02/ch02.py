from typing import Callable, Any
import time 
import functools
import asyncio
from typing import Callable

from util import delay, async_timed


async def my_coroutine() -> None:
    print("Hello World.")


async def add_one(number: int) -> int:
    return number + 1

    
async def long_hello() -> str:
    # await asyncio.sleep(1)
    await delay(1)
    return "Hello World"

    
async def main() -> None:
    one_one = await add_one(1)
    two_one = await add_one(2)
    print(one_one)
    print(two_one)
    
    # for main function, main is blocking with await, but 
    # it also means that main yield execution right back to other parts 
    msg = await long_hello()
    print(f"{msg=}")


async def task():
    # to run tasks concurrently, we need `task`
    sleep_3 = asyncio.create_task(delay(3))
    print(f"type of {type(sleep_3) = }")
    result = await sleep_3
    print(result)

    
async def many_tasks():
    sleep_3 = asyncio.create_task(delay(3))
    sleep_33 = asyncio.create_task(delay(3))
    sleep_333 = asyncio.create_task(delay(3))

    await sleep_3
    # await sleep_33
    # await sleep_333

@async_timed()
async def wait_task():
    delay_task = asyncio.create_task(delay(2))
    
    try:
        res = await asyncio.wait_for(delay_task, timeout=1)
        print(res)
    except asyncio.exceptions.TimeoutError:
        print("Time out.")
        print(f"was the task cancelled? {delay_task.cancelled()}")
    

if __name__ == "__main__":
    
    print(__name__)
    # simple co 
    # asyncio.run(my_coroutine())
    
    # await
    # asyncio.run(main())

    # await
    # asyncio.run(task())

    # concurrent
    # asyncio.run(many_tasks())

    # cancel
    asyncio.run(wait_task())

