import grpc
import json
import banks_pb2
import banks_pb2_grpc

def run_client(input_file):
    # Load input data from the specified JSON file
    with open(input_file) as f:
        data = json.load(f)

    output = []  # Prepare output data structure for storing results

    for entry in data:
        if entry['type'] == 'customer':
            customer_id = entry['id']

            for event in entry['events']:
                # Extract the branch ID and operation details
                branch = event['branch']
                interface = event['interface']
                
                # Connect to the branch server specified by the event's branch ID
                with grpc.insecure_channel(f'localhost:500{branch}') as channel:
                    stub = banks_pb2_grpc.BankStub(channel)
                    
                    # Prepare the response entry for each event
                    response_entry = {
                        "id": customer_id,
                        "recv": []
                    }

                    # Handle each type of interface event
                    if interface == "deposit":
                        # Perform deposit and record the result
                        response = stub.Deposit(banks_pb2.DepositRequest(
                            customer_id=customer_id, event_id=event["id"], amount=event["money"], dest=branch))
                        response_entry["recv"].append({
                            "interface": "deposit",
                            "branch": branch,
                            "result": "success" if response.success else "failed"
                        })

                    elif interface == "withdraw":
                        # Perform withdrawal and record the result
                        response = stub.Withdraw(banks_pb2.WithdrawRequest(
                            customer_id=customer_id, event_id=event["id"], amount=event["money"], dest=branch))
                        response_entry["recv"].append({
                            "interface": "withdraw",
                            "branch": branch,
                            "result": "success" if response.success else "failed"
                        })

                    elif interface == "query":
                        # Perform query and record the balance
                        response = stub.Query(banks_pb2.QueryRequest(
                            customer_id=customer_id, event_id=event["id"], dest=branch))
                        response_entry["recv"].append({
                            "interface": "query",
                            "branch": branch,
                            "balance": response.balance
                        })

                    # Append the response for this event to the output
                    output.append(response_entry)

    # Write the structured output data to output.json
    with open("output.json", "w") as out_file:
        json.dump(output, out_file, indent=4)


if __name__ == "__main__":
    # Execute the client with the specified input file
    run_client("input.json")
