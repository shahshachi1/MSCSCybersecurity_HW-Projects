import grpc
import banks_pb2  # Import the generated messages
import banks_pb2_grpc  # Import the generated gRPC service definitions

class Branch(banks_pb2_grpc.BankServicer):
    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # iterate the processID of the branches
        # TODO: students are expected to store the processID of the branches
        pass

    def Deposit(self, request, context):
        # Logic for handling deposit
        response = banks_pb2.DepositResponse()
        response.result = "success"
        return response


    # TODO: students are expected to process requests from both Client and Branch
    def MsgDelivery(self, request, context):
        pass

    def Query(self, request, context):
        # Implement the logic to handle the Query request
        response = banks_pb2.QueryResponse()
        response.balance = self.balance  # Example logic
        return response

    def Withdraw(self, request, context):
        try:
            if self.balance >= request.money:
                self.balance -= request.money
                response = banks_pb2.WithdrawResponse(result="success")
            else:
                response = banks_pb2.WithdrawResponse(result="insufficient funds")
            return response
        except AttributeError as e:
            context.set_details(f"Error processing request: {e}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return banks_pb2.WithdrawResponse(result="error")


