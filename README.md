# Pond Monitor

A real-time IoT data pipeline built in Python to monitor a water pump via a Shelly smart plug.

Built as a hands-on OOP learning project — every concept here (classes, inheritance, composition, abstract base classes) is grounded in a working system that talks to real hardware.

---

## What it does

Every second, the pipeline:
1. **Collects** — sends an HTTP request to a Shelly Plug S MTR Gen3 and gets back live power, voltage, and current readings
2. **Buffers** — adds the reading to a sliding window (`collections.deque`) that keeps the last 60 seconds of data in memory
3. **Alerts** — compares the latest reading against the rolling average; fires an alert if power spikes above a threshold
4. **Stores** — writes the reading with a timestamp into a local DuckDB database

---

## OOP concepts in play

| Concept | Where |
|---|---|
| **Classes & instances** | `ShellyPlug`, `PowerStream`, `Pipeline`, `DuckDbStorage`, `ConsoleAlerter` |
| **Encapsulation** | Each class owns its state — the plug knows its IP, the stream owns its buffer |
| **Inheritance** | `DuckDbStorage` extends `Storage`; `ConsoleAlerter` extends `Alerter` |
| **Abstract base classes** | `Storage.write()` and `Alerter.send()` raise `NotImplementedError` — subclasses are forced to implement them |
| **Composition** | `Pipeline` is assembled from a plug, stream, storage, and alerter — it doesn't inherit from any of them |
| **Separation of concerns** | Collecting, processing, storing, and alerting are all independent — you can swap any one out without touching the others |

---

## The sliding window (`deque`)

`PowerStream` uses `collections.deque(maxlen=60)` as a circular buffer. When the buffer is full, the oldest reading is automatically dropped as new ones come in — no manual cleanup needed.

This is what makes rolling stats cheap: `mean()`, `max_value()`, and `min_value()` always operate on only the last 60 readings, not the entire history. The full history lives in DuckDB.

```
[t-59] [t-58] ... [t-1] [t]   ← buffer always 60 readings max
                              ↑ new reading pushed here, oldest dropped from left
```

---

## Project structure

```
src/pond_monitor/
├── collectors/
│   └── shelly.py       # HTTP client for Shelly Plug API
├── processing/
│   └── stream.py       # Sliding window buffer + rolling stats
├── storage/
│   ├── base.py         # Abstract Storage base class
│   └── duckdb.py       # DuckDB implementation
├── alerts/
│   ├── base.py         # Abstract Alerter base class
│   └── console.py      # Prints timestamped alerts to terminal
└── pipeline.py         # Orchestrates the ETL loop
main.py                 # Entry point — wires everything together
```

---

## Stack

- **Python 3.12** — managed with `uv`
- **requests** — HTTP calls to the Shelly API
- **DuckDB** — embedded analytical database, no server needed
- **colorlog** — coloured log levels in the terminal (plain text written to file)
- **hatchling** — build backend, `src/` layout

---

## Running it

```bash
uv pip install -e .
python main.py
```

Logs are written to `logs/pipeline.log`. Data is stored in `logs/shelly_plugs.db`.

To query the database after stopping the pipeline:

```python
import duckdb
conn = duckdb.connect("logs/shelly_plugs.db")
conn.execute("SELECT * FROM readings ORDER BY timestamp DESC LIMIT 20").df()
```

> While the pipeline is running, open the connection with `read_only=True` — DuckDB only allows one writer at a time.

---

## Planned improvements

- **Pydantic** — validate Shelly API responses so bad data fails loudly instead of silently writing zeros
- **MotherDuck** — swap `DuckDbStorage("logs/shelly_plugs.db")` for `DuckDbStorage("md:pond_monitor")` for cloud-synced storage
- **Voltage brownout alert** — threshold check on `voltage`, same pattern as the power spike alert
- **5-minute summary log** — periodic stats digest using the rolling window
