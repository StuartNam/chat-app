import time
import random
import socket
from threading import *

# Database
class TokachatDatabase():
    def __init__(self):
        self.lst_accs = [("toka", "1"), ("harryhaha", "anhlaai")]
        self.lst_onl_accs = [] #[username: str, [IP address: str, port: int]]
    
    def load(self, file):
        pass

    def update(self, file):
        pass

# Server sending
class TokachatCentralServer():
    def __init__(self, port, database):
        cs_name = socket.gethostname()
        cs_ipaddr = socket.gethostbyname(cs_name)

        self.addr = (cs_ipaddr, port)
        self.sk = socket.socket()
        self.sk.bind(self.addr)
        self.lst_running_threads = []
        self.lst_done_threads = []
        self.db = database

    def __request_handler(self, csc_conn, c_addr):
        c_req = "null"

        while c_req != "disconn":
            print("CS to {}: Waiting for request ... ".format(c_addr))

            c_req = csc_conn.recv(1024).decode()
            self.__acknowledge(csc_conn)

            if c_req == "disconn":
                # Disconnect from Tokachat
                print("From {}: Disconnect request".format(c_addr))

                csc_conn.close()

                for acc in self.db.lst_onl_accs:
                    _, addr = acc

                    if c_addr[0] == addr[0]:
                        self.db.lst_onl_accs.remove(acc)

                for thread_info in self.lst_running_threads:
                    thread, addr = thread_info

                    if c_addr == addr:
                        self.lst_done_threads.append(thread_info)
                        self.lst_running_threads.remove(thread_info)

            elif c_req == "conn":
                # Connect to another user request
                print("From {}: Connect request".format(c_addr))
                ls_usname = csc_conn.recv(1024).decode()

                print(" - Host username: {}".format(ls_usname))
                flag = False
                for acc in self.db.lst_onl_accs:
                    usname, addr = acc
                    if usname == ls_usname:
                        print(" -> OK")
                        flag = True
                        ls_ipaddr, ls_port = addr

                        # Send address of requested host to client
                        csc_conn.send(ls_ipaddr.encode())
                        self.__confirm_acknowledge(csc_conn)

                        csc_conn.send(str(ls_port).encode())
                        break
                if not flag:
                    print(" -> Failed")
                    csc_conn.send("null".encode())
                    self.__confirm_acknowledge(csc_conn)
                    csc_conn.send("-1".encode())

                print("CS to {}: Done Connect request".format(c_addr))

            elif c_req == "login":
                # Log in request
                print("From {}: Login request".format(c_addr))

                c_usname = csc_conn.recv(1024).decode()
                c_psword = csc_conn.recv(1024).decode()

                c_acc = (c_usname, c_psword)

                print(" - Username: {}\n - Password: {}".format(c_usname, c_psword))
                if c_acc in self.db.lst_accs:
                    print(" -> OK")
                    csc_conn.send("ok".encode())
                else:
                    print(" -> Failed")
                    csc_conn.send("failed".encode())

                print("CS to {}: Done login request".format(c_addr))

            elif c_req == "reg":
                # Register request
                # Exception handling: Not yet
                print("From {}: Register request".format(c_addr))

                usname = csc_conn.recv(1024).decode()
                self.__acknowledge(csc_conn)

                psword = csc_conn.recv(1024).decode()

                acc = [usname, psword]

                print(" - Username: {}\n - Password: {}".format(usname, psword))

                self.db.lst_accs.append(acc)

                csc_conn.send("ok".encode())

                print(" -> OK")

                print("CS to {}: Done Register request".format(c_addr))

            elif c_req == "logout":
                # Log out request
                for acc in self.db.online_accounts:
                    tmp, _ = acc
                    if tmp == addr:
                        self.db.online_accounts.remove(acc)
                        logged_in_flag = False

            elif c_req == "updaddr":
                print("From {}: Update address request".format(c_addr))

                ls_ipaddr = csc_conn.recv(1024).decode()
                self.__acknowledge(csc_conn)

                ls_port = int(csc_conn.recv(1024).decode())
                self.__acknowledge(csc_conn)

                ls_usname = csc_conn.recv(1024).decode()
                self.__acknowledge(csc_conn)

                print(" - Host username: {}".format(ls_usname))
                print(" - Host IP address: {}".format(c_addr))
                print(" - Host port: {}".format(ls_port))

                print(" -> OK")

                self.db.lst_onl_accs.append([ls_usname, (ls_ipaddr, ls_port)])

                print("CS: Done Update address request")

            elif c_req == "gfrlst":
                print("From {}: Get friend list request")

                while True:
                    fd_usname = csc_conn.recv(1024).decode()

                    if fd_usname == "--":
                        break

                    flag = False
                    for acc in self.db.lst_onl_accs:
                        usname, addr = acc
                        ipaddr, port = addr

                        if usname == fd_usname:
                            flag = True

                            csc_conn.send(ipaddr.encode())
                            self.__confirm_acknowledge(csc_conn)

                            csc_conn.send(str(port).encode())

                            break
                    if not flag:
                        csc_conn.send("null".encode())
                        self.__confirm_acknowledge(csc_conn)

                        csc_conn.send("-1".encode())

                print("CS: Done Get friend list request")

            else:
                print("From {}: c_req = {}".format(c_addr, c_req))
                print(" -> Unknown request")
    
    def __acknowledge(self, csc_conn):
        csc_conn.send("ack".encode())
    
    def __confirm_acknowledge(self, csc_conn):
        csc_conn.recv(1024).decode()
        
    def start(self):
        self.sk.listen(100)

        while True:
            time.sleep(1)

            csc_conn, c_addr = self.sk.accept()

            request_handling_thread = Thread(
                target = self.__request_handler,
                args = (csc_conn, c_addr)
            )
            request_handling_thread.start()

            self.lst_running_threads.append((request_handling_thread, c_addr))

            for thread_info in self.lst_done_threads:
                thread, addr = thread_info
                print("Joining thread {}".format(addr))
                thread.join()

def run():
    db = TokachatDatabase()
    db.load("./database.txt")

    Tokachat_central_server = TokachatCentralServer(
        port = 8000,
        database = db
    )

    Tokachat_central_server.start()

    db.update("./database.txt")

if __name__ == "__main__":
    run()