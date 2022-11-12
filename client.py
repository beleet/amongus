
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
			self.channel = grpc.insecure_channel(address)
			self.stub = pb2_grpc.RaftStub(self.channel)

		except grpc.RpcError:
			print("Connection error")
		except Exception as error:
			print(error)

	def get_leader(self):

		if self.channel is not None and self.stub is not None:
			
			message = pb2.EmptyMessage()
			response = self.stub.GetLeader(message)

			print(response)

	def suspend(self):
		pass


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

			elif words[0] == "getleader" and len(words) == 1:
				client.get_leader()

			elif words[0] == "quit" and len(words) == 1:
				print("The client ends")
				break
		
		except KeyboardInterrupt:
			print("The client ends")
			break

