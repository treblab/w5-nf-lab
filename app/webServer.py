#import socket module
from socket import *

# Create server socket (TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 6789  # any port > 1024 should be fine
serverSocket.bind(('', serverPort))

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
sys.exit()  # terminate the program after sending the corresponding data


# URL:
# http://192.168.1.160:6789/webPage.html

# Command to run the server:
# python3 -m http.server 6789