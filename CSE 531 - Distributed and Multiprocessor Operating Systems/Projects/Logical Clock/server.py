import grpc
from concurrent import futures
import json
import sys
import banks_pb2_grpc
import banks_pb2
from branch import Branch
from threading import Lock
import time

# Lock to ensure safe access to test_2.json
file_lock = Lock()

all_events = []  # New global list to capture all events for `test3.json`

class BankService(banks_pb2_grpc.BranchServiceServicer):
    def __init__(self, branch_id, balance):
        self.branch = Branch(branch_id, balance)
        self.branch_id = branch_id
        self.events = []  # Store events for this branch

    def log_event(self, customer_request_id, logical_clock, interface, comment):
        event = {
            "customer-request-id": customer_request_id,
            "logical_clock": logical_clock,
            "interface": interface,
            "comment": comment
        }
        self.events.append(event)
        all_events.append({**event, "id": self.branch_id, "type": "branch"})
        print(f"All events so far: {all_events}")  # Debug print to confirm events are added
        self.save_event_to_file(event)

    def save_event_to_file(self, event):
        # Append this event to `test_2.json` as before
        with file_lock:
            try:
                with open("test_2.json", "a") as f:
                    json.dump({
                        "id": self.branch_id,
                        "type": "branch",
                        "event": event
                    }, f)
                    f.write(",\n")  # Separate events with a comma
                    print(f"Event for branch {self.branch_id} saved.")  # Debug message
            except Exception as e:
                print(f"Error saving event for branch {self.branch_id}: {e}")

    def Deposit(self, request, context):
        self.branch.logical_clock = max(self.branch.logical_clock, request.logical_clock) + 1
        self.log_event(
            customer_request_id=request.customer_id,
            logical_clock=self.branch.logical_clock,
            interface="deposit",
            comment=f"event_recv from customer {request.customer_id}"
        )
        return banks_pb2.Response(success=True, logical_clock=self.branch.logical_clock)

    def Withdraw(self, request, context):
        self.branch.logical_clock = max(self.branch.logical_clock, request.logical_clock) + 1
        self.log_event(
            customer_request_id=request.customer_id,
            logical_clock=self.branch.logical_clock,
            interface="withdraw",
            comment=f"event_recv from customer {request.customer_id}"
        )
        return banks_pb2.Response(success=True, logical_clock=self.branch.logical_clock)

    def Propagate(self, request, context):
        self.branch.logical_clock = max(self.branch.logical_clock, request.logical_clock) + 1
        self.log_event(
            customer_request_id=request.customer_request_id,
            logical_clock=self.branch.logical_clock,
            interface=f"propagate_{request.action}",
            comment=f"event_recv from branch {request.branch_id}"
        )
        return banks_pb2.Response(success=True, logical_clock=self.branch.logical_clock)

def save_test3():
    with open('test3.json', 'w') as f:
        json.dump(all_events, f, indent=4)
    print("test3.json generated successfully with the following data:", all_events)

def serve(branch_id, balance):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bank_service = BankService(branch_id, balance)
    banks_pb2_grpc.add_BranchServiceServicer_to_server(bank_service, server)
    port = 5000 + branch_id
    server.add_insecure_port(f'0.0.0.0:{port}')
    print(f"Starting branch server {branch_id} on port {port}")

    # Start the server
    server.start()

    if branch_id == 1:
        with file_lock:
            with open("test_2.json", "w") as f:
                f.write("[\n")
        print("Initialized test_2.json with opening bracket")

    print(f"Branch server {branch_id} is running on port {port}...")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print(f"Branch server {branch_id} shutting down.")
    finally:
        if branch_id == 4:
            with file_lock:
                with open("test_2.json", "rb+") as f:
                    f.seek(-2, 2)
                    f.truncate()
                    f.write(b"\n]")
            print("Finalized test_2.json with closing bracket")
            save_test3()  # Ensure `test3.json` is generated on final shutdown

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python server.py <branch_id> <balance>")
        sys.exit(1)

    branch_id = int(sys.argv[1])
    balance = int(sys.argv[2])

    serve(branch_id, balance)
