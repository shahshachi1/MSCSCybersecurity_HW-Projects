How to Run:

1. Create Python Environment
	- in project's folder, open terminal
	- command: 'python3 -m venv project2'
	- command: bash
	- command: project2/bin/activate

2. Generate the banks_pb2_grpc.py and banks_pb2.py files
	- command: python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/banks.proto

3. Run the Server
	- in one terminal run: python server.py 1 400
	- in another terminal run: python server.py 2 400
	- in another terminal run: python server.py 3 400
	- in another terminal run: python server.py 4 400

4. Run the Client
	- command: python client.py input.py

5. Compare the output with the test checkers:
	- command: python checker_part_1.py test_1.json
	- command: python checker_part_2.py test_2.json
	- command: python checker_part_3.py test_3.json
