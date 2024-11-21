How to Run:

1. Create Python Environment
	- in project's folder, open terminal
	- command: 'python3 -m venv project3'
	- command: bash
	- command: project3/bin/activate

2. Generate the banks_pb2_grpc.py and banks_pb2.py files
	- command: python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/banks.proto

3. Run the Server
	- in one terminal run: python server.py 1 0
	- in another terminal run: python server.py 2 0
	- in another terminal run: python server.py 3 0
	- in another terminal run: python server.py 4 0
	- in another terminal run: python server.py 5 0
	- in another terminal run: python server.py 6 0
	- in another terminal run: python server.py 7 0
	- in another terminal run: python server.py 8 0
	- in another terminal run: python server.py 9 0
	- in another terminal run: python server.py 10 0

4. Run the Client
	- command: python client.py input.py

