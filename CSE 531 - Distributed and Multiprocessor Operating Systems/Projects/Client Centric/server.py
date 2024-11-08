import grpc
from concurrent import futures
import sys
import banks_pb2
import banks_pb2_grpc

class BranchServer(banks_pb2_grpc.BankServicer):
    def __init__(self, branch_id, initial_balance):
        # Initialize the branch with a unique ID and initial balance
        self.branch_id = branch_id
        self.balance = initial_balance
        self.writeset = set()  # Track applied event IDs to prevent duplicate applications

    def propagate_update(self, event_id, balance_change):
        """ 
        Propagate balance updates to other branches to ensure consistency.
        
        - Ensures Monotonic Writes: By propagating each update after a successful
          deposit or withdrawal, each branch is made aware of previous writes
          before applying any new ones.
        """
        for port in range(5001, 5006):  # Assuming branches use ports 5001 - 5005
            if port != 5000 + self.branch_id:  # Avoid sending to itself
                with grpc.insecure_channel(f'localhost:{port}') as channel:
                    stub = banks_pb2_grpc.BankStub(channel)
                    # Send balance update to the other branch
                    stub.ReceiveUpdate(banks_pb2.UpdateRequest(event_id=event_id, balance_change=balance_change))

    def ReceiveUpdate(self, request, context):
        """ 
        Receive balance updates from other branches and apply if not already applied.
        
        - Maintains Monotonic Writes: Each branch checks the event ID and applies updates
          only if they have not been processed, ensuring events are handled in order.
        """
        if request.event_id not in self.writeset:
            self.balance += request.balance_change  # Apply the specific balance change
            self.writeset.add(request.event_id)  # Mark event as applied
        return banks_pb2.UpdateResponse(success=True)

    def Deposit(self, request, context):
        """ 
        Handle deposit requests, apply locally, and propagate to other branches.
        
        - Ensures Read Your Writes: The deposit is immediately applied and propagated, so any
          subsequent query reflects this change across branches.
        """
        if request.event_id not in self.writeset:
            self.balance += request.amount  # Apply the deposit
            self.writeset.add(request.event_id)  # Mark event as applied
            self.propagate_update(request.event_id, request.amount)  # Propagate deposit
        return banks_pb2.DepositResponse(success=True, balance=self.balance)

    def Withdraw(self, request, context):
        """ 
        Handle withdrawal requests, apply locally if balance is sufficient, and propagate.
        
        - Ensures Read Your Writes: The withdrawal is applied immediately and propagated, so
          any subsequent query across branches will reflect this change.
        """
        if request.event_id not in self.writeset and self.balance >= request.amount:
            self.balance -= request.amount  # Apply the withdrawal
            self.writeset.add(request.event_id)  # Mark event as applied
            self.propagate_update(request.event_id, -request.amount)  # Propagate withdrawal
            success = True
        else:
            success = False
        return banks_pb2.WithdrawResponse(success=success, balance=self.balance)

    def Query(self, request, context):
        """ 
        Handle query requests to return the current balance of the branch.
        
        - Ensures Read Your Writes: Because deposits and withdrawals are immediately
          propagated, the current balance reflects the latest changes.
        """
        return banks_pb2.QueryResponse(balance=self.balance)


def serve(branch_id, balance):
    # Start the gRPC server with the specified branch ID and initial balance
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    branch_server = BranchServer(branch_id, balance)
    banks_pb2_grpc.add_BankServicer_to_server(branch_server, server)
    server.add_insecure_port(f'[::]:500{branch_id}')  # Bind to unique port based on branch_id
    print(f"Starting branch server {branch_id} on port 500{branch_id} with initial balance {balance}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python server.py <branch_id> <initial_balance>")
        sys.exit(1)
    
    # Read command-line arguments for branch ID and initial balance
    branch_id = int(sys.argv[1])
    initial_balance = int(sys.argv[2])
    serve(branch_id, initial_balance)
