from collections import deque
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PowerStream:
    def __init__(self, plug: str, maxlen: int = 60):
        self.plug = plug
        self.buffer = deque(maxlen=maxlen)

    def add_reading(self, reading):
        reading["timestamp"] = datetime.now()
        reading["plug_name"] = self.plug
        self.buffer.append(reading)
    
    def mean(self, field):
        if not self.buffer:
            return None
        return sum(r[field] for r in self.buffer) / len(self.buffer)
    
    def max_value(self, field):
        if not self.buffer:
            return None
        return max(r[field] for r in self.buffer)
    
    def min_value(self, field):
        if not self.buffer:
            return None
        return min(r[field] for r in self.buffer)