import logging
import os
import colorlog
from pond_monitor.collectors.shelly import ShellyPlug
from pond_monitor.processing.stream import PowerStream
from pond_monitor.storage.duckdb import DuckDbStorage
from pond_monitor.alerts.console import ConsoleAlerter
from pond_monitor.pipeline import Pipeline


def main():
    os.makedirs("logs", exist_ok=True)

    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        }
    ))

    file_handler = logging.FileHandler("logs/pipeline.log")
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler]
    )

    print("Hello from the ShellyPlug data extractor! Logging is included")
    # bedroom fan
    plug = ShellyPlug(ip_address="192.168.129.20", name="bedroom_fan", device_id="0")
    stream = PowerStream(plug, maxlen=60)  # 1 minute window
    alerter = ConsoleAlerter()
    with DuckDbStorage("logs/shelly_plugs.db") as storage:
        pipeline = Pipeline(plug, stream, storage, alerter)
        pipeline.run()

if __name__ == "__main__":
    main()
