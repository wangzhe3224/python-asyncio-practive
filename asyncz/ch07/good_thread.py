import threading
import socket
import logging


class ClientEchoThread(threading.Thread):

    def __init__(self, client: socket.socket):
        super().__init__()
        self.client = client

    def run(self):

        try:
            while True:
                data = self.client.recv(2048)
                if not data:
                    raise BrokenPipeError("Connection closed.")
                print(f"Received {data}")
                # echo back to client
                self.client.sendall(data)
        except OSError as e:
            logging.error(f"Thread interrputed by {e} Exception, shutting down.")

    def close(self):
        if self.is_alive():
            self.client.sendall(bytes("Shutting down!", encoding="utf-8"))
            self.client.shutdown(socket.SHUT_RDWR)