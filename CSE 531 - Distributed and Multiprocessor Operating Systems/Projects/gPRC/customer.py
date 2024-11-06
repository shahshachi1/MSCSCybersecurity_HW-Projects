import grpc
import banks_pb2
import banks_pb2_grpc

class Customer:
    def __init__(self, id, stub):
        self.id = id
        self.stub = stub

    def executeEvents(self, events):
        for event in events:
            # Apply modulo operation
            customer_id = self.id % 50
            if customer_id == 0:
                customer_id = 50

            if event['interface'] == 'deposit':
                print(f"Sending deposit event for Customer ID: {customer_id}")
                response = self.stub.Deposit(banks_pb2.DepositRequest(customer_id=customer_id, amount=event["money"]))
                print(f"Received response: {response.result}")

            elif event['interface'] == 'query':
                print(f"Sending query event for Customer ID: {customer_id}")
                response = self.stub.Query(banks_pb2.QueryRequest(customer_id=customer_id))
                print(f"Query response for Customer ID: {customer_id} - Balance: {response.balance}")

            elif event['interface'] == 'withdraw':
                print(f"Sending withdraw event for Customer ID: {customer_id}")
                response = self.stub.Withdraw(banks_pb2.WithdrawRequest(customer_id=customer_id, amount=event['money']))
                print(f"Received response: {response.result}")
