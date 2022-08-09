import asyncio
from concurrent.futures import Future
from asyncio import AbstractEventLoop
from typing import Callable, Optional
from aiohttp import ClientSession
from threading import Thread

from queue import Queue
from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import ttk


class StressTest:

    def __init__(self,
                 loop: AbstractEventLoop,
                 url: str,
                 total_request: int,
                 callback: Callable[[int, int], None]):
        self._completed_request: int = 0
        self._refresh_rate = total_request // 100
        self._total_request = total_request
        self._callback = callback
        self._url = url
        self._loop = loop
        self._load_test_future: Optional[Future] = None

    def start(self):
        fut = asyncio.run_coroutine_threadsafe(self._make_request(), self._loop)
        self._load_test_future = fut

    def cancel(self):
        if self._load_test_future:
            self._loop.call_soon_threadsafe(self._load_test_future.cancel)

    async def _get_url(self, sess: ClientSession, url: str):
        try:
            await sess.get(url)
        except Exception as e:
            print(e)

        self._completed_request += 1
        if self._completed_request % self._refresh_rate == 0 \
                or self._completed_request == self._total_request:
            print(f"Computed: {self._completed_request} / {self._total_request}")
            self._callback(self._completed_request, self._total_request)

    async def _make_request(self):
        async with ClientSession() as sess:
            reqs = [self._get_url(sess, self._url) for _ in range(self._total_request)]
            await asyncio.gather(*reqs)


class LoadTester(Tk):

    def __init__(self, loop, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self._queue = Queue()
        self._refresh_ms = 25

        self._loop = loop
        self._load_test: Optional[StressTest] = None
        self.title("URL Requester")

        self._url_label = Label(self, text="URL:")
        self._url_label.grid(column=0, row=0)

        self._url_field = Entry(self, width=10)
        self._url_field.grid(column=1, row=0)

        self._request_field = Entry(self, width=10)
        self._request_field.grid(column=1, row=1)

        self._submit = ttk.Button(self, text="Submit", command=self._start)
        self._submit.grid(column=2, row=1)

        self._pb_label = Label(self, text="Progress: ")
        self._pb_label.grid(column=0, row=3)

        self._pb = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self._pb.grid(column=1, row=3, columnspan=2)

    def _update_bar(self, pct: int):
        if pct == 100:
            self._load_test = None
            self._submit["text"] = "Submit"
        else:
            self._pb["value"] = pct
            self.after(self._refresh_ms, self._poll_queue)

    def _queue_update(self, completed_requests: int, total_requests: int):
        self._queue.put(int(completed_requests / total_requests * 100))

    def _poll_queue(self):
        if not self._queue.empty():
            pct_complete = self._queue.get()
            self._update_bar(pct_complete)
        else:
            if self._load_test:
                self.after(self._refresh_ms, self._poll_queue)

    def _start(self):
        if self._load_test is None:
            self._submit['text'] = 'Cancel'
            test = StressTest(self._loop, self._url_field.get(), int(self._request_field.get()), self._queue_update)
            self.after(self._refresh_ms, self._poll_queue)
            test.start()
            self._load_test = test
        else:
            self._load_test.cancel()
            self._load_test = None
            self._submit['text'] = 'Submit'


class ThreadedEventLoop(Thread):

    def __init__(self, loop: AbstractEventLoop):
        super().__init__()
        self._loop = loop
        self.deamon = True

    def run(self):
        self._loop.run_forever()


if __name__ == '__main__':

    loop = asyncio.new_event_loop()
    async_thread = ThreadedEventLoop(loop)
    async_thread.start()

    app = LoadTester(loop)
    app.mainloop()