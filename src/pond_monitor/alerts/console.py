from datetime import datetime
from .base import Alerter


class ConsoleAlerter(Alerter):
    def send(self, message):
        print(f"[{datetime.now()}] {message}")