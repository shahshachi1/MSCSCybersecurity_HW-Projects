import grpc
from concurrent import futures
import time
import banks_pb2
import banks_pb2_grpc

class BankService(banks_pb2_grpc.BankServicer):
    def __init__(self):
        self.customers = {}

    def Deposit(self, request, context):
        if request.id not in self.customers:
            self.customers[request.id] = 0.0
        self.customers[request.id] += request.money
        return banks_pb2.DepositResponse(result="success", new_balance=self.customers[request.id])

    def Withdraw(self, request, context):
        if request.id not in self.customers or self.customers[request.id] < request.money:
            return banks_pb2.WithdrawResponse(result="failure", new_balance=self.customers.get(request.id, 0.0))
        self.customers[request.id] -= request.money
        return banks_pb2.WithdrawResponse(result="success", new_balance=self.customers[request.id])

    def Query(self, request, context):
        balance = self.customers.get(request.id, 0.0)
        return banks_pb2.QueryResponse(balance=balance)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    banks_pb2_grpc.add_BankServicer_to_server(BankService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051.")
    try:
        while True:
            time.sleep(86400)  # Keep server running for a day
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
