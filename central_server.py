import socket
from threading import *

# Database

accounts = [("tokarinrika", "liliana0"), ("harryhaha", "anhlaai")]
active_threads = []
done_threads = []
active_accounts = [] #(IP address, username)
# Server sending
def server_feedback(connection, msg):
    conn, _ = connection
    conn.send(msg.encode())

def server_request_handler(connection):
    logged_in_flag = False
    conn, addr = connection
    client_request = 1
    server_signal = 0
    
    while client_request != 0:
        client_request = int.from_bytes(conn.recv(1024))
        if client_request == 0:
            if logged_in_flag:
            # Disconnect request
            # Send disconnect message to send thread and disconnect   
                pass
            else:
                msg = "Disconnect from server"
                server_feedback(connection, msg)
                for active_thread in active_threads:
                    _, conn = active_thread
                    if conn == connection:
                        done_threads.append(active_thread)
                        active_threads.remove(active_thread)

        elif client_request == 1:
            server_feedback(server_signal)
            # Connect request
            pass
        elif client_request == 2:
            # Log in request
            username = conn.recv(1024).decode()
            password = conn.recv(1024).decode()
            account_info = (username, password)
            if account_info in accounts:
                active_accounts.append((addr, username))
                msg = "Log in successfully"
                logged_in_flag = True
                server_feedback(conn, msg)
            else:
                msg = "Log in failed"
                server_feedback(conn, msg)
        elif client_request == 3:
            # Register request
            username = conn.recv(1024).decode()
            password = conn.recv(1024).decode()
            account_info = (username, password)
            accounts.append(account_info)
            msg = "Register successfully"
            server_feedback(conn, msg)
        elif client_request == 4:
            # Log out request
            for acc in active_accounts:
                tmp, _ = acc
                if tmp == addr:
                    active_accounts.remove(acc)
                    logged_in_flag = False

# Handlers
def mainloop():
    host = socket.gethostname()
    port = 8000

    cserver_socket = socket.socket()
    cserver_socket.bind((host, port))
    cserver_socket.listen()

    while True:
        connection = cserver_socket.accept()

        thread_server_request_handler = Thread(
            target = server_request_handler,
            args = (connection, )
        )
        thread_server_request_handler.start()

        active_threads.append((thread_server_request_handler, connection))

        for server_threads in done_threads:
            server_threads.join()

if __name__ == "__main__":
    mainloop()
