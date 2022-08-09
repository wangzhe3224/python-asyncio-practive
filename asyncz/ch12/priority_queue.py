import asyncio
from asyncio import Queue, PriorityQueue
from typing import Tuple


async def worker(queue: Queue):
    while not queue.empty():
        work_item: Tuple[int, str] = await queue.get()
        print(f"Processing work item {work_item}")
        queue.task_done()


async def main():
    pq = PriorityQueue()

    work_items = [(3, 'Lowest priority'),
                  (2, 'Medium priority'),
                  (1, 'High priority')]

    worker_task = asyncio.create_task(worker(pq))
    for w in work_items:
        pq.put_nowait(w)

    await asyncio.gather(pq.join(), worker_task)


asyncio.run(main())