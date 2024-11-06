import grpc
import json
import banks_pb2
import banks_pb2_grpc
from customer import Customer

def run():
    # Establish connection with gRPC server
    channel = grpc.insecure_channel('localhost:50051')  # Ensure server is running
    stub = banks_pb2_grpc.BankServiceStub(channel)

    # Load the input JSON file
    with open('input.json', 'r') as f:
        data = json.load(f)

    output_data = []

    # Process customers
    for customer_data in data:
        if customer_data['type'] == 'customer':
            customer_id = customer_data['id']
            
            # Apply modulo 50 logic, with a fix for IDs that are multiples of 50
            customer_id = customer_id % 50
            if customer_id == 0:
                customer_id = 50

            events = customer_data['events']
            customer = Customer(customer_id, events, stub)
            customer_output = customer.executeEvents()

            output_data.append({'id': customer_id, 'recv': customer_output})

    # Write output to output.json
    with open('output.json', 'w') as f:
        json.dump(output_data, f, indent=4)

class Customer:
    def __init__(self, customer_id, events, stub):
        self.customer_id = customer_id
        self.events = events
        self.stub = stub

    def executeEvents(self):
        responses = []
        for event in self.events:
            if event['interface'] == 'deposit':
                response = self.stub.Deposit(banks_pb2.DepositRequest(customer_id=self.customer_id, amount=event['money']))
                responses.append({'interface': 'deposit', 'result': response.result})

            elif event['interface'] == 'query':
                response = self.stub.Query(banks_pb2.QueryRequest(customer_id=self.customer_id))
                responses.append({'interface': 'query', 'balance': response.balance})

            elif event['interface'] == 'withdraw':
                response = self.stub.Withdraw(banks_pb2.WithdrawRequest(customer_id=self.customer_id, amount=event['money']))
                responses.append({'interface': 'withdraw', 'result': response.result})

        return responses

if __name__ == '__main__':
    run()
