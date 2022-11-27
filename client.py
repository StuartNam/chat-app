"""
Client Side:

    Client connects to central server, send request to server to perform something
    A request contains 2 parts: request and info of request (string or int)
    Send a request to a server means send 2 parts sequentially.
    Client must:
        - Log in:
            Send log in request to server:
                request: int (2)
                username: str
                password: str
        - Disconnect:
                request: int (0)
                No additional info
        - Register:
                request: int (3)
                username: str
                password: str
        - Log out:
                request: int (4)
                No additional info
            
"""
import socket

def log_in():
    pass

server_ip = socket.gethostname()
port = 8000

client_cserver_socket = socket.socket()
client_cserver_socket.connect((server_ip, port))