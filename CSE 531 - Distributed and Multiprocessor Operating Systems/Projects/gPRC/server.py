import grpc
from concurrent import futures
import banks_pb2_grpc
from branch import Branch

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    banks_pb2_grpc.add_BankServiceServicer_to_server(Branch(), server)
    server.add_insecure_port('[::]:50051')
    print("Server is running on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
