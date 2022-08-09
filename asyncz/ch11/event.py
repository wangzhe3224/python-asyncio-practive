import asyncio
import functools
from asyncio import Event, StreamWriter, StreamReader


class FileUpload:

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self._reader = reader
        self._writer = writer
        self._finished_event = Event()
        self._buffer = b""
        self._upload_task = None

    def listen_for_uploads(self):
        self._upload_task = asyncio.create_task(self._accept_upload())

    async def _accept_upload(self):
        while data := await self._reader.read(1024):
            self._buffer += data
        self._finished_event.set()
        self._writer.close()
        await self._writer.wait_closed()

    async def get_content(self):
        await self._finished_event.wait()
        return self._buffer


class FileServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.upload_event = Event()

    async def start_server(self):
        server = await asyncio.start_server(self._client_connected, self.host, self.port)
        await server.serve_forever()

    async def dump_contents_on_complete(self, upload: FileUpload):
        file_content = await upload.get_content()
        print(file_content)

    def _client_connected(self, reader: StreamReader, writer: StreamWriter):
        upload = FileUpload(reader, writer)
        upload.listen_for_uploads()
        asyncio.create_task(self.dump_contents_on_complete(upload))