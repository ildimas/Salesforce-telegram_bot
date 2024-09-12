import asyncio

class AsyncDict:
    def __init__(self):
        self._dict = {}
        self._lock = asyncio.Lock()  # Ensure thread-safe operations

    async def set(self, key, value):
        async with self._lock:
            self._dict[key] = value
            print(f"Set {key}: {value}")

    async def get(self, key):
        async with self._lock:
            return self._dict.get(key, None)

    async def delete(self, key):
        async with self._lock:
            if key in self._dict:
                del self._dict[key]
                print(f"Deleted {key}")

    async def keys(self):
        async with self._lock:
            return list(self._dict.keys())

    async def values(self):
        async with self._lock:
            return list(self._dict.values())

    async def items(self):
        async with self._lock:
            return list(self._dict.items())