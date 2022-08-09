import sys
import asyncio
from asyncio import StreamReader
from asyncz.util import delay


async def main():
    while True:
        delay_time: int = int(input(f"Enter a time to sleep: "))
        asyncio.create_task(delay(delay_time))


async def create_stdin_reader() -> StreamReader:
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    loop = asyncio.get_event_loop()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)

    return reader


async def command_line():
    stdin_reader = await create_stdin_reader()
    while True:
        delay_time = await stdin_reader.readline()
        asyncio.create_task(delay(int(delay_time)))


if __name__ == '__main__':

    # asyncio.run(main())
    asyncio.run(command_line())