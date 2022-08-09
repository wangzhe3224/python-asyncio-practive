import asyncio
import aiohttp
from aiohttp import ClientSession
from asyncz.util import async_timed, logger


@async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    async with session.get(url) as result:
        return result.status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "http://www.google.com"
        status = await fetch_status(session, url)
        logger.info(f"Status for {url} was {status}")


asyncio.run(main())
