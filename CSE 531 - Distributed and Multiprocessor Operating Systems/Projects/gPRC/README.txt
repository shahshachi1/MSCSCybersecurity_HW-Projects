How to Run:

1. Create Python Environment
	- in project's folder, open terminal
	- command: 'python3 -m venv project1'
	- command: bash
	- command: project1/bin/activate

2. Generate the banks_pb2_grpc.py and banks_pb2.py files
	- command: python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/banks.proto

3. Run the Server
	- in one terminal run: python server.py 1
	- in another terminal run: python server.py 2
	- in another terminal run: python server.py 3
	- in another terminal run: python server.py 4

4. Run the Client
	- command: python client.py input.py
