import time
from collections import OrderedDict
from typing import Any, Optional, Tuple


class LRUCacheTTL:
    def __init__(self, capacity: int, ttl: float):
        self.capacity = capacity
        self.ttl = ttl
        # key (chave) -> (value, timestamp)
        self.data: OrderedDict[str, Tuple[Any, float]] = OrderedDict()

    def _is_expired(self, timestamp: float) -> bool:
        return (time.time() - timestamp) > self.ttl

    def get(self, key: str) -> Optional[Any]:
        if key not in self.data:
            return None
        value, ts = self.data[key]
        if self._is_expired(ts):
            # Remove itns expirados
            self.data.pop(key)
            return None
        # Move para o fim os mais recentes usados
        self.data.move_to_end(key)
        return value

    def put(self, key: str, value: Any) -> None:
        now = time.time()
        if key in self.data:
            # Atualiza existente
            self.data.move_to_end(key)
            self.data[key] = (value, now)
        else:
            if len(self.data) >= self.capacity:
                # Remove os recentes menos usados
                self.data.popitem(last=False)
            self.data[key] = (value, now)

    def invalidate(self, key: str) -> None:
        self.data.pop(key, None)

    def clear(self) -> None:
        self.data.clear()
