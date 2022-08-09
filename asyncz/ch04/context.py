import asyncio
import socket
from types import TracebackType
from typing import Optional, Type

from asyncz.util import logger


class ConnectedSocket:
    
    def __init__(self, server_socket) -> None:
        self._conn = None
        self._server_socket = server_socket
        
    async def __aenter__(self):
        logger.info(f"Entering context manager, waiting for connection")
        loop = asyncio.get_event_loop()
        conn, addr = await loop.sock_accept(self._server_socket)
        self._conn = conn 
        logger.info(f"Accept a connection")
        return self._conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.info(f"Exit context manager")
        self._conn.close()
        logger.info(f"Connection closed.")
        

async def main():
    loop = asyncio.get_event_loop()
    
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    async with ConnectedSocket(server_socket=server_socket) as conn:
        data = await loop.sock_recv(conn, 1024)
        print(data)
        
        
asyncio.run(main())