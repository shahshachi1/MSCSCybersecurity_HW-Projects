# output_logger.py
import json

class OutputLogger:
    def __init__(self):
        self.events = []

    def log_event(self, event):
        """Log a single event."""
        self.events.append(event)

    def save_to_file(self, filename="output.json"):
        """Write all events to output.json."""
        with open(filename, 'w') as f:
            json.dump(self.events, f, indent=4)
        print(f"Saved {len(self.events)} events to {filename}")
