#!/usr/bin/env python3
import socket, time, sys
from multiprocessing import Process

# Define address & buffer size
HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024

# TODO: getRemoteIP() method
# Get IP
def getRemoteIP(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

# TODO: handleRequest() method
# Send connections back to client
def handleRequest(addr, conn):
	print("Connected by ", addr)

	full_data = conn.recv(BUFFER_SIZE)
	conn.sendall(full_data)
	conn.shutdown(socket.SHUT_RDWR)
	conn.close()

def main():
	# TODO: Establish localhost, extern_host (google), port, buffer size
	extern_host = "www.google.com"
	port = 80

	# Create socket
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start: # Establish "start" of proxy (connects to localhost)
		# TODO: bind and set to listening mode
		print("Starting proxy server")

		# Allow reused addresses, bind and set to listening mode
		proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		proxy_start.bind((HOST, PORT))
		proxy_start.listen(1)

		while True:
			# TODO: accept incoming connections from proxy_start, print information about connection
			# Connect proxy_start
			conn, addr = proxy_start.accept()
			print("Connected by ", addr)

			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end: # Establish "end" of proxy (connects to google)
				# TODO: get remote IP of google, connect proxy_end to it
				print("Connecting to Google")
				remote_ip = getRemoteIP(extern_host)

				# Connect proxy_end
				proxy_end.connect((remote_ip, port))

				# Send data
				send_full_data = conn.recv(BUFFER_SIZE)
				print(f"Sending recieved data {send_full_data} to google")
				proxy_end.sendall(send_full_data)

				# Remember to shut down
				proxy_end.shutdown(socket.SHUT_WR) # shutdown() is different from close()

				data = proxy_end.recv(BUFFER_SIZE)
				print(f"Sending recieved data {data} to client")

				# Send data back
				conn.send(data)

				# Now for the multiprocessing...

				# TODO: allow for multiple connections with a Process daemon
				# Make sure to set target = handleRequest when creating the Process
				p = Process(target=handleRequest, args=(addr, conn))
				p.daemon = True
				p.start()
				print("Started process ", p)

			# TODO: close the connection!
			conn.close()

if __name__ == "__main__":
	main()