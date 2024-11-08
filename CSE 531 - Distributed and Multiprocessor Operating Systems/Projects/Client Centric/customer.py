class Customer:
    def __init__(self, customer_id, events):
        self.customer_id = customer_id
        self.events = events
        self.writeset = set()

    def add_event(self, event):
        self.events.append(event)
