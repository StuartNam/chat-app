import socket
from threading import *

# Database

accounts = []
active_threads = []
active_conns = []
active_user = [] #(username, IP address)
# Server sending
def server_feedback():
    signal = True
    pass

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
    cserver_socket.bind((host, port))
    cserver_socket.listen()

    while True:
        conn, addr = cserver_socket.accept()
        thread_send = Thread()

if __name__ == "__main__":
    mainloop()




