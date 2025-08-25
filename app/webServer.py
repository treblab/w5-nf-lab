#import socket module
from socket import *

# Create server socket (TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 6789  # any port > 1024 should be fine
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        # Receive request message from the client
        message = connectionSocket.recv(1024).decode()

        # Extract filename from the request
        filename = message.split()[1]
 
        f = open(filename[1:], 'rb')  # open in binary mode
        outputdata = f.read()
        connectionSocket.send(b"HTTP/1.1 200 OK\r\n\r\n")
        print("HTTP 200: File found and sent successfully.")
        connectionSocket.send(outputdata)

    except IOError:
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        print("HTTP 404: File not found.")
        connectionSocket.send("<html><h1>404 Not Found</h1></html>".encode())

        # Close client socket
        connectionSocket.close()
        
serverSocket.close()
sys.exit()  # terminate the program after sending the corresponding data


# URL:
# http://192.168.1.160:6789/webPage.html

# Command to run the server:
# python3 -m http.server 6789