#import socket module
from socket import *
import sys  # for terminating the program

# Create server socket (TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 6789  # you can choose any available port >1024
serverSocket.bind(('', serverPort))
serverSocket.listen(1)  # max 1 queued connection``

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        # Receive request message from the client
        message = connectionSocket.recv(1024).decode()

        # Extract filename from the request
        filename = message.split()[1]
        f = open(filename[1:])  # remove leading '/'

        # Read the file and prepare response
        outputdata = f.read()

        # Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        # Send the content of the requested file
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError:
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><h1>404 Not Found</h1></html>".encode())

        # Close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()  # Terminate the program after sending the data
