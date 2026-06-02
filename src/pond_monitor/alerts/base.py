class Alerter:
    
    def send(self, message):
        raise NotImplementedError("Alerter subclasses must implement the send method")