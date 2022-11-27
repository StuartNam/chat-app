import socket
from threading import *

# Database

accounts = []
active_threads = []
active_conns = []

# Handler

def connect_handler(conn):
    pass

def login_handler(username, password):
    account = (username, password)
    if account in accounts:
        server_feedback("Log in successfully")
    else:
        server_feedback("Log in failed")
# Server sending
def server_feedback():
    signal = True
    while 

def server_receive(conn):
    client_request = 1
    server_signal = 0

    while client_request != 0:
        client_request = int.from_bytes(conn.recv(1024))
        if client_request == 0:
            # Disconnect request
            # Send disconnect message to send thread and disconnect
            server_feedback(server_signal)
            pass
        elif client_request == 1:
            server_feedback(server_signal)
            # Connect request
            pass
        elif client_request == 2:
            # Log in request
            server_feedback(server_signal)
            pass
        elif client_request == 3:
            # Register request
            pass
        elif client_request == 4:
            # Log out request
            pass

# Handlers
def mainloop():
    host = socket.gethostname()
    port = 8000

    cserver_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen()

    while True:
        conn, addr = server_socket.accept()
        thread_send = threading.Thread()




