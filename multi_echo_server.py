#!/usr/bin/env python3
import socket
from multiprocessing import Process

# Define address & buffer size
HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024

# Echo connections back to client
def handleEcho(addr, conn):
	print("Connected by ", addr)

	full_data = conn.recv(BUFFER_SIZE)
	conn.sendall(full_data)
	conn.shutdown(socket.SHUT_RDWR)
	conn.close()

def main():
	# Create socket, bind and set to listening mode
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# Allow reused addresses
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen(2)

		while True:
			# Accept connections and start a Process daemon for handling multiple connections
			conn, addr = s.accept()
			p = Process(target=handleEcho, args=(addr, conn))
			p.daemon = True
			p.start()
			print("Started process ", p)

if __name__ == "__main__":
	main()