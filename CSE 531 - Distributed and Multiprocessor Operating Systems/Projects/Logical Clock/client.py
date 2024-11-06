import grpc
import json
import sys
import banks_pb2
import banks_pb2_grpc
import time

class Customer:
    def __init__(self, customer_id):
        self.id = customer_id
        self.logical_clock = 0

    def increment_clock(self):
        self.logical_clock += 1

    def send_request(self, stub, interface, amount, request_id):
        self.increment_clock()
        print(f"Customer {self.id} sending {interface} of {amount} with logical clock {self.logical_clock}")

        if interface == "deposit":
            request = banks_pb2.DepositRequest(
                customer_id=self.id,
                amount=amount,
                logical_clock=self.logical_clock
            )
            response = stub.Deposit(request)
        elif interface == "withdraw":
            request = banks_pb2.WithdrawRequest(
                customer_id=self.id,
                amount=amount,
                logical_clock=self.logical_clock
            )
            response = stub.Withdraw(request)
        else:
            raise ValueError("Invalid interface")

        self.logical_clock = max(self.logical_clock, response.logical_clock)

        customer_event = {
            "customer-request-id": request_id,
            "logical_clock": self.logical_clock,
            "interface": interface,
            "comment": f"event_sent from customer {self.id}"
        }
        customer_events[self.id].append(customer_event)
        all_events.append({**customer_event, "id": self.id, "type": "customer"})

        return response.success

def connect_to_branch_ports(branch_ports):
    branch_stubs = {}
    for branch_id, port in branch_ports.items():
        channel = grpc.insecure_channel(f'localhost:{port}')
        stub = banks_pb2_grpc.BranchServiceStub(channel)
        branch_stubs[branch_id] = stub
    return branch_stubs

def run_customers(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    branch_ports = {1: 5001, 2: 5002, 3: 5003, 4: 5004}
    branch_stubs = connect_to_branch_ports(branch_ports)

    global customer_events, all_events
    customer_events = {entry['id']: [] for entry in data if entry['type'] == 'customer'}
    branch_events = {branch_id: [] for branch_id in branch_ports.keys()}
    all_events = []

    for entry in data:
        if entry['type'] == 'customer':
            customer = Customer(entry['id'])
            for request in entry['customer-requests']:
                interface = request['interface']
                amount = request['money']
                request_id = request['customer-request-id']

                success = customer.send_request(branch_stubs[1], interface, amount, request_id)

                primary_event = {
                    "customer-request-id": request_id,
                    "logical_clock": customer.logical_clock,
                    "interface": interface,
                    "comment": f"event_recv from customer {customer.id}"
                }
                branch_events[1].append(primary_event)
                all_events.append({**primary_event, "id": 1, "type": "branch"})

                for propagate_branch in branch_ports.keys():
                    if propagate_branch != 1:
                        stub = branch_stubs[propagate_branch]
                        customer.increment_clock()
                        print(f"Customer {customer.id} propagating {interface} to branch {propagate_branch} with clock {customer.logical_clock}")

                        propagate_request = banks_pb2.PropagateRequest(
                            branch_id=1,
                            customer_request_id=request_id,
                            amount=amount,
                            action=interface,
                            logical_clock=customer.logical_clock
                        )

                        response = stub.Propagate(propagate_request)
                        customer.logical_clock = max(customer.logical_clock, response.logical_clock)

                        propagate_event = {
                            "customer-request-id": request_id,
                            "logical_clock": customer.logical_clock,
                            "interface": f"propagate_{interface}",
                            "comment": f"event_sent to branch {propagate_branch}"
                        }
                        branch_events[1].append(propagate_event)
                        all_events.append({**propagate_event, "id": 1, "type": "branch"})

                        receive_event = {
                            "customer-request-id": request_id,
                            "logical_clock": response.logical_clock,
                            "interface": f"propagate_{interface}",
                            "comment": f"event_recv from branch 1"
                        }
                        branch_events[propagate_branch].append(receive_event)
                        all_events.append({**receive_event, "id": propagate_branch, "type": "branch"})

    test_1_output = [
        {"id": customer_id, "type": "customer", "events": events}
        for customer_id, events in customer_events.items()
    ]
    with open('test_1.json', 'w') as f:
        json.dump(test_1_output, f, indent=4)

    test_2_output = [
        {"id": branch_id, "type": "branch", "events": events}
        for branch_id, events in branch_events.items()
    ]
    with open('test_2.json', 'w') as f:
        json.dump(test_2_output, f, indent=4)

    with open('test_3.json', 'w') as f:
        json.dump(all_events, f, indent=4)

    # Combine all test files into one sorted output
    combine_test_outputs()

    print("\nSummary:")
    print(f"Customer events written to test_1.json")
    print(f"Branch events written to test_2.json")
    print(f"All events written to test_3.json")
    print(f"Combined events written to output.json")

def combine_test_outputs():
    combined_events = []

    with open('test_1.json', 'r') as f:
        test_1_data = json.load(f)
        for customer in test_1_data:
            for event in customer["events"]:
                combined_events.append({**event, "id": customer["id"], "type": "customer"})

    with open('test_2.json', 'r') as f:
        test_2_data = json.load(f)
        for branch in test_2_data:
            for event in branch["events"]:
                combined_events.append({**event, "id": branch["id"], "type": "branch"})

    with open('test_3.json', 'r') as f:
        test_3_data = json.load(f)
        combined_events.extend(test_3_data)

    # Sort all events by logical clock
    combined_events.sort(key=lambda x: x["logical_clock"])

    with open('output.json', 'w') as f:
        json.dump(combined_events, f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <input_file>")
        sys.exit(1)

    run_customers(sys.argv[1])
