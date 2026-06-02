import requests
import logging

logger = logging.getLogger(__name__)

class ShellyPlug:
    def __init__(self, ip_address: str, name: str, device_id: str = "0"):
        self.ip_address = ip_address
        self.name = name
        self.device_id = device_id
        self.base_url = f"http://{ip_address}/rpc" 

    def _make_request(self, endpoint):
        logger.debug("attempting connection to %s at %s", self.name, self.ip_address)
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url)
            logger.info("Successfully connected to %s at %s", self.name, self.ip_address)
            return response.json()
        except requests.exceptions.ConnectionError:
            # print(f"Could not reach {self.name} at {self.ip_address}")
            logger.error("Connection error while trying to reach %s at %s", self.name, self.ip_address)
            return None

    def get_status(self):
        return self._make_request(f"Switch.GetStatus?id={self.device_id}")

    def turn_on(self):
        return self._make_request(f"Switch.Set?id={self.device_id}&on=true")

    def turn_off(self):
        return self._make_request(f"Switch.Set?id={self.device_id}&on=false")   