
import raft_pb2 as pb2 
import raft_pb2_grpc as pb2_grpc

import grpc 


class Client:

	def __init__(self):
		self.host = "127.0.0.1"
		self.channel = None
		self.stub = None

	def connect(self, address):

		try:
			print("Connection")

			self.channel = grpc.insecure_channel(address)
			self.stub = pb2_grpc.RaftStub(self.channel)

			message = pb2.EmptyMessage()
			response = self.stub.GetLeader(message)

			print(response)
		except grpc.RpcError:
			print(f"The server {address} is unavailable")
		except Exception as error:
			print(error)


if __name__ == "__main__":

	client = Client()
	print("Client starts")

	while True:
		
		try:
			message = input("> ")
			words = message.split()

			if len(words) == 0:
				print("")
				continue

			if words[0] == "connect" and len(words) == 2:
				client.connect(words[1])
		
		except KeyboardInterrupt:
			print("The client ends")
			break

