from asyncio import Semaphore
import asyncio


async def operation(semaphore: Semaphore):
    print(f"Waiting to acquire semaphore...")
    async with semaphore:
        print(f"Semaphore acquried!")
        await asyncio.sleep(2)
    print(f"Released Semaphore!")


async def main():
    semaphore = Semaphore(2)
    await asyncio.gather(*[operation(semaphore) for _ in range(5)])


asyncio.run(main())