import asyncio
from asyncio.subprocess import Process


async def main():
    process: Process = await asyncio.create_subprocess_exec("ls", "-l")
    print(f"Process id is : {process.pid}")
    status_code = await process.wait()
    print(f"Status Code: {status_code}")


asyncio.run(main())