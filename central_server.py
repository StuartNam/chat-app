import socket
from threading import *

# Database

accounts = [("toka", "1"), ("harryhaha", "anhlaai")]
active_threads = []
done_threads = []
active_accounts = [] #(IP address, username)
# Server sending
def cserver_feedback(conn, sig, msg):
    conn.send(sig.encode())
    conn.send(msg.encode())

def cserver_request_handler(conn, addr):
    logged_in_flag = False
    client_request = "something"
    server_signal = 0

    while client_request != "disconn":
        print("Waiting for request ... ")
        client_request = conn.recv(1024).decode()
        conn.send("ok".encode())
        if client_request == "disconn":
            if logged_in_flag:
            # Disconnect from central server request
            # Send disconnect message to send thread and disconnect   
                pass
            else:
                msg = "Disconnect from application"
                cserver_feedback(connection, msg)
                for active_thread in active_threads:
                    _, conn = active_thread
                    if conn == connection:
                        done_threads.append(active_thread)
                        active_threads.remove(active_thread)

        elif client_request == "conn":
            # Connect to another user request
            print("Client requests: Connect")
            s_usname = conn.recv(1024).decode()
            flag = False
            for active_account in active_accounts:
                addr, name = active_account
                if name == s_usname:
                    flag = True
                    s_ipaddr, s_port = addr
                    conn.send(s_ipaddr.encode())
                    conn.recv(1024)
                    conn.send(str(s_port).encode())
                    break
            if not flag:
                conn.send("null".encode())
                conn.recv(1024)
                conn.send("-1".encode())

        elif client_request == "login":
            # Log in request
            print("Client requests: Login")
            username = conn.recv(1024).decode()
            password = conn.recv(1024).decode()
            account_info = (username, password)
            print(account_info)
            if account_info in accounts:
                sig = "ok"
                logged_in_flag = True
                conn.send(sig.encode())
            else:
                sig = "failed"
                conn.send(sig.encode())
            print("End login")

        elif client_request == "reg":
            # Register request
            username = conn.recv(1024).decode()
            password = conn.recv(1024).decode()
            account_info = (username, password)
            accounts.append(account_info)
            msg = "Register successfully"
            cserver_feedback(conn, msg)
        elif client_request == "logout":
            # Log out request
            for acc in active_accounts:
                tmp, _ = acc
                if tmp == addr:
                    active_accounts.remove(acc)
                    logged_in_flag = False
        elif client_request == "disconns":
            pass
            #Disconnect from server request
        elif client_request == "updaddr":
            print("Client requests: Update address")
            s_ipaddr = conn.recv(1024).decode()
            conn.send("ok".encode())
            s_port = conn.recv(1024).decode()
            conn.send("ok".encode())
            s_usname = conn.recv(1024).decode()
            conn.send("ok".encode())
            print(((s_ipaddr, int(s_port)), s_usname))
            active_accounts.append(((s_ipaddr, int(s_port)), s_usname))
            print("End update address")
        elif client_request == "gfrlst":
            print("Client requests: Get friends status")
            while True:
                fr_usname = conn.recv(1024).decode()
                if fr_usname == "--":
                    break
                flag = False
                for active_account in active_accounts:
                    addr, usname = active_account
                    ipaddr, port = addr
                    if usname == fr_usname:
                        flag = True
                        conn.send(ipaddr.encode())
                        conn.recv(1024)
                        conn.send(str(port).encode())
                        break
                if not flag:
                    conn.send("null".encode())
                    conn.recv(1024)
                    conn.send("-1".encode())
            print("End get friend list")
        else:
            print("Request = " + client_request)
            print("Wrong request")


def mainloop():
    cs_host_name = socket.gethostname()
    cs_host_ipaddr = socket.gethostbyname(cs_host_name)
    cs_port = 8000

    print("Server host:", cs_host_ipaddr, cs_port)
    cserver_socket = socket.socket()
    cserver_socket.bind((cs_host_ipaddr, cs_port))
    cserver_socket.listen()

    while True:
        conn, addr = cserver_socket.accept()

        thread_cserver_request_handler = Thread(
            target = cserver_request_handler,
            args = (conn, addr)
        )
        thread_cserver_request_handler.start()

        active_threads.append((thread_cserver_request_handler, conn, addr))

        for server_threads in done_threads:
            server_threads.join()

if __name__ == "__main__":
    mainloop()
