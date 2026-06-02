# Improvements Backlog

## Storage
- [ ] Switch to MotherDuck by changing `DuckDbStorage("logs/pond.db")` to `DuckDbStorage("md:pond_monitor")` in `main.py` — no other changes needed
- [ ] Validate Shelly API response shape using Pydantic models — ensures bad/missing data is caught at the boundary before entering the pipeline. 📚 [Pydantic on RealPython](https://realpython.com/python-pydantic/)

## Alerting
- [ ] Alert if voltage drops below `min_value("voltage")` — could indicate a brownout
- [ ] Log a periodic summary every 5 minutes: "last 60s — avg: 245W, max: 312W, min: 198W"

## Logging
- [ ] Replace basicConfig string format with JSON logging via `python-json-logger`

## Python Tips & Lessons

### List Comprehension vs Generator Expression

```python
# # python# with list comprehension (creates a list first, then sums)
sum([r[field] for r in self.buffer])

# with generator expression (more memory efficient)
sum(r[field] for r in self.buffer)
# The difference is subtle — a generator doesn't build the whole list in memory first. For 60 readings it doesn't matter, but it's a good habit. Add it to docs/improvements.md for now. ✅with list comprehension (creates a list first, then sums)
sum([r[field] for r in self.buffer])

# with generator expression (more memory efficient)
sum(r[field] for r in self.buffer)
```

The difference is subtle — a generator doesn't build the whole list in memory first. For 60 readings it doesn't matter, but it's a good habit. ✅

---

### Type Hints — Making Intent Explicit

Python doesn't enforce what type you pass into a function. `self.plug` is just whatever object you pass in at runtime. Type hints make the intention explicit for readers and editors — but don't enforce anything at runtime.

```python
# Without type hints — works, but unclear what's expected
def __init__(self, plug, stream, storage, alerter):
    self.plug = plug

# With type hints — clear contract, editor autocomplete works
from pond_monitor.collectors.shelly import ShellyPlug
from pond_monitor.processing.stream import PowerStream

def __init__(self, plug: ShellyPlug, stream: PowerStream, ...):
    self.plug = plug
```

The connection between `self.plug` and `ShellyPlug` is made in `main.py` when you wire it all together:

```python
plug = ShellyPlug("192.168.1.100", "pond_pump")
pipeline = Pipeline(plug, stream, storage, alerter)
# now self.plug IS a ShellyPlug — because you passed one in
```

📚 RealPython: [Python Type Checking](https://realpython.com/python-type-checking/)

