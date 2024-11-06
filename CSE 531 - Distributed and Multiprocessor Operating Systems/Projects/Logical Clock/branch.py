import banks_pb2
import banks_pb2_grpc

class Branch:
    def __init__(self, branch_id, initial_balance, logical_clock=0):
        self.id = branch_id
        self.balance = initial_balance
        self.logical_clock = logical_clock
    
    def increment_clock(self):
        self.logical_clock += 1

    def handle_deposit(self, request, context):
        self.increment_clock()
        self.balance += request.amount
        self.logical_clock = max(self.logical_clock, request.logical_clock)
        return banks_pb2.Response(success=True, logical_clock=self.logical_clock)

    def handle_withdraw(self, request, context):
        self.increment_clock()
        if self.balance >= request.amount:
            self.balance -= request.amount
            self.logical_clock = max(self.logical_clock, request.logical_clock)
            return banks_pb2.Response(success=True, logical_clock=self.logical_clock)
        else:
            return banks_pb2.Response(success=False, logical_clock=self.logical_clock)

    def propagate(self, request, context):
        self.increment_clock()
        self.logical_clock = max(self.logical_clock, request.logical_clock)
        if request.action == "deposit":
            self.balance += request.amount
        else:
            self.balance -= request.amount
        return banks_pb2.Response(success=True, logical_clock=self.logical_clock)
