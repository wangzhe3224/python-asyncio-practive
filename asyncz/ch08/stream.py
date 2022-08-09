import asyncio
from asyncio import StreamReader
from typing import AsyncGenerator


async def read_until_empty(steam_reader: StreamReader) -> AsyncGenerator[str, None]:
    while response := await steam_reader.readline():
        yield response.decode()


async def main():
    host = "www.google.com"
    request = f"GET / HTTP/1.1\r\n" \
              f"Connection: close\r\n" \
              f"Host: {host}\r\n\r\n"
    reader, writer = await asyncio.open_connection(host, 80)

    try:
        writer.write(request.encode())
        await writer.drain()

        res = [res async for res in read_until_empty(reader)]

        print("".join(res))
    finally:
        writer.close()
        await writer.wait_closed()


asyncio.run(main())
