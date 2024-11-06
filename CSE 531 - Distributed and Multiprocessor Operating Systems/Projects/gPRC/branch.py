import banks_pb2
import banks_pb2_grpc

class Branch(banks_pb2_grpc.BankServiceServicer):
    def __init__(self, initial_balance=400):
        self.balance = initial_balance

    def Deposit(self, request, context):
        self.balance += request.amount
        print(f"Deposit: Customer {request.customer_id} deposited {request.amount}. New balance: {self.balance}")
        return banks_pb2.DepositResponse(result="success")

    def Withdraw(self, request, context):
        if self.balance >= request.amount:
            self.balance -= request.amount
            print(f"Withdraw: Customer {request.customer_id} withdrew {request.amount}. New balance: {self.balance}")
            return banks_pb2.WithdrawResponse(result="success")
        else:
            print(f"Withdraw: Customer {request.customer_id} insufficient funds for {request.amount}. Balance remains {self.balance}")
            return banks_pb2.WithdrawResponse(result="insufficient funds")

    def Query(self, request, context):
        print(f"Query: Customer {request.customer_id} queried balance. Current balance: {self.balance}")
        return banks_pb2.QueryResponse(balance=self.balance)
