from http import server
import selectors
import socket 
from selectors import SelectorKey
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger()

selector = selectors.DefaultSelector()

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.setblocking(False)
server_socket.bind(server_address)
server_socket.listen()

selector.register(server_socket, selectors.EVENT_READ)

while True:
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)  # timeout 1 sec
    
    if (len(events)) == 0:
        logger.info(f"No event, wait...")

    for event, _ in events:
        event_socket = event.fileobj
        
        if event_socket == server_socket:
            # get a client connection
            conn, addr = server_socket.accept()
            conn.setblocking(False)
            print(f"I got a new connection from {addr}")
            selector.register(conn, selectors.EVENT_READ)
        else:
            # get a client data
            data = event_socket.recv(1024)
            print(f"I got some data: {data}, echo back to client")
            event_socket.send(data)