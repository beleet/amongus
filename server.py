
import raft_pb2 as pb2 
import raft_pb2_grpc as pb2_grpc

import grpc
import sys
import random

from concurrent import futures


CONFIG = "config.conf"

def handler():

	class Raft(pb2_grpc.RaftServicer):

		def __init__(self):

			self.term = 0
			self.delay = random.randrange(150, 300) / 1000
			
			self.state = 0		# 0 - Follower, 1 - Candidate, 2 - Leader
			self.is_voted = False
			self.vote_counter = 0
			
			self.current_leader_id = None
			self.current_leader_address = None

		def GetLeader(self, request, context):

			print("Getting leader")

			leader = {"id": current_leader_id, "address": current_leader_address}
			return pb2.LeaderResponse(**leader)


	server_id = sys.argv[1]
	host, port = None, None

	with open(CONFIG) as config:

		for line in config:
			
			tokens = line.split()

			if tokens[0] == server_id:
				
				if len(tokens) != 3:
					raise Exception("Invalid config line: {line}")

				host, port = tokens[1], tokens[2]
				break

	if host is None or port is None:
		print(f"{host}:{port}")
		raise Exception("Wrong port or host")

	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	pb2_grpc.add_RaftServicer_to_server(Raft(), server)
	server.add_insecure_port(f"[::]:{port}")

	server.start()

	print(f"Server started at {host}:{port}")

	server.wait_for_termination()


if __name__ == "__main__":
	handler()
