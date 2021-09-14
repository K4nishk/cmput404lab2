#!/usr/bin/env python3
import socket, time, sys
from multiprocessing import Process

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

	# Create socket
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start: # Establish "start" of proxy (connects to localhost)
		# TODO: bind and set to listening mode

		while True:
			# TODO: accept incoming connections from proxy_start, print information about connection

			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end: # Establish "end" of proxy (connects to google)
				# TODO: get remote IP of google, connect proxy_end to it

				# Now for the multiprocessing...

				# TODO: allow for multiple connections with a Process daemon
				# Make sure to set target = handleRequest when creating the Process

			# TODO: close the connection!

if __name__ == "__main__":
	main()