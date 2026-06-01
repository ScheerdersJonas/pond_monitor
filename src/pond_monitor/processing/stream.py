from collections import deque

class PowerStream:
    def __init__(self, plug, maxlen=60):
        self.plug = plug
        self.buffer = deque(maxlen=maxlen)