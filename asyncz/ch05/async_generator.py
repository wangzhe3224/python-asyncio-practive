from typing import AsyncGenerator
import asyncio
from asyncz.util import delay, async_timed


async def positive_integer(until: int):
    for i in range(1, until):
        await delay(i)
        yield i


async def take(gen: AsyncGenerator, to_take: int):
    counter = 0
    async for item in gen:
        if counter > to_take - 1:
            return
        counter += 1
        yield item


@async_timed()
async def main():
    a_gen = positive_integer(3)

    print(type(a_gen))
    async for i in a_gen:
        print(f"Got number {i}.")

    b_gen = positive_integer(10)

    async for i in take(b_gen, 3):
        print(i)


asyncio.run(main())