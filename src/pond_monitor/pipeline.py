from .collectors.shelly import ShellyPlug
from .processing.stream import PowerStream
from .storage.duckdb import DuckDbStorage
import logging
import time

logger = logging.getLogger(__name__)

class Pipeline:
    def __init__(self, plug: ShellyPlug, stream: PowerStream, storage: DuckDbStorage , alerter, power_threshold=1.5):
        self.plug = plug
        self.stream = stream
        self.storage = storage
        self.alerter = alerter
        self.power_threshold = power_threshold

    def etl(self):
        status = self.plug.get_status()

        if status is None:
            self.alerter.send(f"Failed to get status from {self.plug.name}")
            return
        
        reading = {
            "apower": status.get("apower", 0),
            "voltage": status.get("voltage", 0),
            "current": status.get("current", 0)
        }

        logger.info("Collected data from %s: %s", self.plug.name, reading)
        self.stream.add_reading(reading)
        avg = self.stream.mean("apower")
        if avg is not None and reading["apower"] > self.power_threshold * avg:
            self.alerter.send(f"High power alert for {self.plug.name}: {reading['apower']}W")

        logger.info("Processed data for %s: %s", self.plug.name, reading)

        self.storage.write(reading)
        logger.info("Stored data for %s", self.plug.name)

    def run(self):
        while True:
            self.etl()
            time.sleep(1)  # Run every second