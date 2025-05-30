#Module for socket communication for DVA248 Datorsystem
#
#   author: Dag Nystrom, 2023
#
import socket
import pickle

##########################
#### SERVER-SIDE FUNCTIONS
##########################

def serverInitSocket (ip='127.0.0.1', port=12347):
    '''
    Server-side function to create a socket for new client connections.
        ip:     a string containing the IP address to the server, default is localhost.
        port:   an int containing the port to listen to, default is 12345
    Returns a socket object
    '''
    serverSocket: socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)

    return server_socket

def serverWaitForNewClient(serverSocket:socket):
    '''
    Server-side function that makes the server wait for a new client connecting on the server socket.
        serverSocket:   the socket used for new client connections
    Returns a socket to the new client
    '''
    clientSocket:socket
    client_socket, client_address = serverSocket.accept()
    print(f"New connection from {client_address}")
    
    return client_socket

def serverSendString(clientSocket:socket, mess:str):
    '''
    Server-side function to transmit a string from the server to the client via the client socket
        clientSocket:   the socket to transmit on
        mess:           the message to transmit
    '''
#   Note: Function must transform UNICODE strings to byte strings
    small_message = mess.encode('utf-8')
    clientSocket.sendall(small_message)

    return

def serverRecvPlanet(clientSocket:socket):
    '''
    Server-side function to receive a planet object from a client over the client socket.
    The function waits until it receives a planet.
        clientSocket:   the socket to receive from
    Returns the planet object
    '''
#   Note: Function must recreate object from bytestring
    data = b''
    while True:
        packet = clientSocket.recv(4096)
        if not packet:
            break
        data += packet
        try:
            planet = pickle.loads(data)
            return planet
        except (pickle.UnpicklingError, EOFError):
            continue




#########################
### CLIENT-SIDE FUNCTIONS
#########################

def clientInitSocket (ip='127.0.0.1',port=12347):
    '''
    Client-side function to connect to a server via its connecting socket
        ip:     a string containing the IP address to the server, default is localhost
        port:   and integer with the portnumber to use, default is 12345
    Returns a client socket to communicate with the server over
    '''
    clientSocket:socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    return client_socket

def clientRecvString(clientSocket:socket):
    '''
    Client-side function to receive a string from the server over a socket
        clientSocket:   the socket used for communication with the server
    Returns the string.
    '''
    message:str
    data = clientSocket.recv(4096)
    return data.decode('utf-8')

def clientSendPlanet(clientSocket:socket, p:object):
    '''
    Client-side function to send a planet object to the server over a socket
        clientSocket:   the socket used for communication with the server
        p:              the planet object to transmit'''
#   Note: Function must transform object into bytestring
    convert_byte = pickle.dumps(p)
    clientSocket.sendall(convert_byte)

    return

    
    