class Branch:
    def __init__(self, branch_id, initial_balance):
        self.branch_id = branch_id
        self.balance = initial_balance
        self.writeset = set()

    def process_deposit(self, event_id, amount):
        if event_id not in self.writeset:
            self.balance += amount
            self.writeset.add(event_id)
            return True, self.balance
        return False, self.balance

    def process_withdraw(self, event_id, amount):
        if event_id not in self.writeset and self.balance >= amount:
            self.balance -= amount
            self.writeset.add(event_id)
            return True, self.balance
        return False, self.balance

    def process_query(self):
        return self.balance
