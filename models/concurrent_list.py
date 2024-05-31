import threading


class ConcurrentList:
    def __init__(self):
        self.list = []
        self.lock = threading.Lock()

    def append(self, item):
        with self.lock:
            self.list.append(item)

    def get(self, index):
        with self.lock:
            return self.list[index]

    def __len__(self):
        with self.lock:
            return len(self.list)

    def get_last(self):
        with self.lock:
            if len(self.list) > 0:
                return self.list[-1]
            else:
                raise IndexError("get_last from empty list")

    def remove(self, item):
        with self.lock:
            self.list.remove(item)

    def pop(self, index=-1):
        with self.lock:
            if len(self.list) > 0:
                return self.list.pop(index)
            else:
                raise IndexError("pop from empty list")

    def clear(self):
        with self.lock:
            self.list.clear()

    def __iter__(self):
        with self.lock:
            # Create a copy of the list to iterate over to prevent race conditions
            # This avoids holding the lock for the entire duration of iteration
            return iter(self.list.copy())

    def __str__(self):
        with self.lock:
            return str(self.list)
