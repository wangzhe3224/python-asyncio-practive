from threading import Lock
from typing import List


class IntListThreadSafe:

    def __init__(self, wrapped_list: List[int]):
        self._lock = Lock()
        self._inner_list = wrapped_list

    def indices_of(self, to_find: int):
        with self._lock:
            enum = enumerate(self._inner_list)
            return [index for index, value in self._inner_list if value == to_find]
