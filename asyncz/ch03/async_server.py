from asyncio import AbstractEventLoop
import asyncio
from contextlib import AbstractAsyncContextManager
from http import server
import socket
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger()


async def echo(conn: socket, loop: AbstractEventLoop):
    while data := await loop.sock_recv(conn, 1024):
        await loop.sock_sendall(conn, data)


async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    
    while True:
        conn, addr = await loop.sock_accept(server_socket)
        conn.setblocking(False)
        logger.info(f"Got a connection from {addr}")
        asyncio.create_task(echo(conn, loop))

async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    addr = ("127.0.0.1", 8000)
    server_socket.setblocking(False)
    server_socket.bind(addr)
    server_socket.listen()
    
    await listen_for_connection(server_socket=server_socket, loop=asyncio.get_event_loop())

    
asyncio.run(main())

# This is because we’ve kept a reference around to the task. 
# asyncio can only print this message and the traceback for a failed task when that task is garbage collected.