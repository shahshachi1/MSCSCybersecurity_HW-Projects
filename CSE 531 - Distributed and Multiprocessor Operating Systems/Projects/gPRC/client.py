import json
import grpc
import banks_pb2
import banks_pb2_grpc

def main():
    # Create a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')
    stub = banks_pb2_grpc.BankStub(channel)

    output_data = []

    # Load input data
    with open('input.json') as f:
        requests = json.load(f)

    for req in requests:
        customer_id = req["id"]
        customer_output = {"id": customer_id, "recv": []}

        # Deposit money if specified
        if "deposit" in req:
            deposit_response = stub.Deposit(banks_pb2.DepositRequest(id=customer_id, money=req["deposit"]))
            customer_output["recv"].append({
                "interface": "deposit",
                "result": deposit_response.result
            })

        # Query balance
        query_response = stub.Query(banks_pb2.QueryRequest(id=customer_id))
        customer_output["recv"].append({
            "interface": "query",
            "balance": query_response.balance
        })

        # Withdraw money if specified
        if "withdraw" in req:
            withdraw_response = stub.Withdraw(banks_pb2.WithdrawRequest(id=customer_id, money=req["withdraw"]))
            customer_output["recv"].append({
                "interface": "withdraw",
                "result": withdraw_response.result
            })
            # Query balance again after withdrawal
            query_response = stub.Query(banks_pb2.QueryRequest(id=customer_id))
            customer_output["recv"].append({
                "interface": "query",
                "balance": query_response.balance
            })

        # Append this customer's output to the main output list
        output_data.append(customer_output)

    # Write output to JSON file
    with open('output.json', 'w') as f:
        json.dump(output_data, f, indent=4)

    print("Output written to output.json")

if __name__ == '__main__':
    main()
