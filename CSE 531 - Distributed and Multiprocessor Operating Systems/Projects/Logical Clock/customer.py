import banks_pb2
import banks_pb2_grpc

class Customer:
    def __init__(self, customer_id, requests):
        self.id = customer_id
        self.requests = requests
        self.logical_clock = 0
    
    def increment_clock(self):
        self.logical_clock += 1

    def send_request(self, stub, request_type, amount):
        self.increment_clock()
        if request_type == "deposit":
            request = banks_pb2.DepositRequest(customer_id=self.id, amount=amount, logical_clock=self.logical_clock)
            response = stub.Deposit(request)
        else:  # withdraw
            request = banks_pb2.WithdrawRequest(customer_id=self.id, amount=amount, logical_clock=self.logical_clock)
            response = stub.Withdraw(request)
        
        # Synchronize logical clocks
        self.logical_clock = max(self.logical_clock, response.logical_clock)
        return response
