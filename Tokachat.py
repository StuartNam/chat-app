import tkinter as tk
from threading import *
import socket
import random

root = tk.Tk()

class TokachatUser():
    def __init__(self):
        pass


def on_closing():
    global req
    global program_phase
    global ccs_socket
    global lst_done_threads

    req = "disconn"
    program_phase = True

    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

"""
    GLOBAL VARIABLE
"""
logged_in = False
program_phase = False
server_phase = False

req = ""
c_req = ""
req_args = []
c_login_usname = ""
c_login_psword = ""
c_usname = ""
connected_usname = ""
cs_res = ""
cs_msg = ""
cs_socket = 0
ccs_socket = 0
sc_socket = 0

lst_running_threads = []
lst_done_threads = []

c_lst_friends = []
c_msg_histories = []

def upd_friend_status_request(ccs_socket):
    global c_lst_friends

    c_req = "updfrstt"
    ccs_socket.send(c_req.encode())
    ccs_socket.recv(1024)
    for friend in c_lst_friends:
        _, fd_usname = friend
        ccs_socket.send(fd_usname.encode())
        fd_ipaddr = ccs_socket.recv(1024).decode()

        ccs_socket.send("ok".encode())
        fd_port = int(ccs_socket.recv(1024).decode())

        friend[0][0] = fd_ipaddr
        friend[0][1] = fd_port
        print(friend)

    ccs_socket.send("--".encode())
    grid_friend_list()

def connect_server_request(ccs_socket, s_usname):
    global lbl_chat_detail
    global lbl_chat_usname
    global txt_chat_prompt
    global connected_usname
    global btn_send
    global btn_attach_file

    c_req = "conn"
    ccs_socket.send(c_req.encode())
    ccs_socket.recv(1024)
    ccs_socket.send(s_usname.encode())

    s_ipaddr = ccs_socket.recv(1024).decode()
    ccs_socket.send("ok".encode())
    s_port = int(ccs_socket.recv(1024).decode())

    if (s_ipaddr != "null"):
        cs_socket = socket.socket()
        cs_socket.connect((s_ipaddr, s_port))
        lbl_chat_usname.config(text = s_usname)
        lbl_chat_detail.config(text = "Connected")
        btn_send.config(state = "normal")   
        btn_attach_file.config(state = "normal")
        txt_text_prompt.delete("1.0", tk.END)
        load_chat_promt(s_usname)
        connected_usname = s_usname
        return cs_socket
    else:
        print("Connection failed")
        lbl_chat_usname.config(text = s_usname)
        lbl_chat_detail.config(text = "Not connected")

        txt_chat_prompt.config(state = "normal")
        txt_chat_prompt.delete("1.0", tk.END)
        txt_chat_prompt.config(state = "disabled")

        btn_send.config(state = "disabled")
        btn_attach_file.config(state = "disabled")
        return -1

def disconnect_server_request(ccs_socket):
    c_req = "disconn"
    ccs_socket.send(c_req.encode())
    ccs_socket.recv(1024)

def send_msg(cs_socket):
    global txt_chat_prompt
    global txt_text_prompt
    global c_usname
    global c_msg_histories

    print("Sending message ...")
    c_req = "send"
    msg = txt_text_prompt.get("1.0", tk.END)
    txt_text_prompt.delete("1.0", tk.END)
    cs_socket.send(c_req.encode())
    cs_socket.recv(1024).decode()
    cs_socket.send(c_usname.encode())
    receiver_usname = cs_socket.recv(1024).decode()
    cs_socket.send(msg.encode())
    cs_socket.recv(1024)

    txt_chat_prompt.config(state = "normal")
    txt_chat_prompt.insert(tk.END, "Me: {}\n".format(msg))
    txt_chat_prompt.config(state = "disabled")

    flag = False
    for c_msg_history in c_msg_histories:
        if (receiver_usname == c_msg_history[0]):
            flag = True
            c_msg_history[1].append("Me: " + msg)
            break
    if not flag:
        c_msg_histories.append([receiver_usname, ["Me: " + msg]])
    print(c_msg_histories)

def get_friend_list_request(ccs_socket):
    global c_lst_friends
    global c_usname

    c_req = "gfrlst"
    ccs_socket.send(c_req.encode())
    ccs_socket.recv(1024).decode()
    ccs_socket.send(c_usname.encode())
    fd_usname = ""
    while True:
        fd_usname = ccs_socket.recv(1024).decode()
        
        print(fd_usname)

        if fd_usname == "--":
            break
        ccs_socket.send("ack".encode())
        c_lst_friends.append([["null", "-1"], fd_usname])

def server_host():
    global sc_socket
    global ccs_socket
    global program_phase
    global lst_done_threads
    global lst_running_threads

    while program_phase:
        continue

    # Send server address
    print("Sending address ...")
    s_host_name = socket.gethostname()
    s_ipaddr = socket.gethostbyname(s_host_name)
    s_port = random.randint(49152, 65535)

    sc_socket = socket.socket()
    sc_socket.bind((s_ipaddr, s_port))

    c_req = "updaddr"
    ccs_socket.send(c_req.encode())
    ccs_socket.recv(1024)
    ccs_socket.send(s_ipaddr.encode())
    ccs_socket.recv(1024)
    ccs_socket.send(str(s_port).encode())
    ccs_socket.recv(1024)
    ccs_socket.send(c_usname.encode())
    ccs_socket.recv(1024)
    
    program_phase = True
    sc_socket.listen()
    while True:
        sc_conn, cc_addr = sc_socket.accept()
        print("Server host: Accept connect request")
        s_req_handler_thread = Thread(
            target = server_request_handler,
            args = (sc_conn, cc_addr)
        )
        s_req_handler_thread.start()

        lst_running_threads.append((s_req_handler_thread, cc_addr))

        for thread_info in lst_done_threads:
            thread, addr = thread_info
            print("Joining thread {}".format(addr))
            thread.join()

def program():
    # Connect to central server 
    global logged_in
    global program_phase
    global c_login_usname
    global c_login_psword
    global cs_res
    global cs_msg
    global c_usname
    global c_lst_friends
    global req
    global ccs_socket
    global cs_socket
    global sc_socket

    cs_host_name = socket.gethostname()
    cs_ipaddr = socket.gethostbyname(cs_host_name)
    cs_port = 8000

    ccs_socket = socket.socket()
    ccs_socket.connect((cs_ipaddr, cs_port))

    # Login or register
    while not logged_in:
        while not program_phase:
            continue

        c_req = "login"
        ccs_socket.send(c_req.encode())
        ccs_socket.recv(1024)
        ccs_socket.send(c_login_usname.encode())
        ccs_socket.send(c_login_psword.encode())

        cs_res = ccs_socket.recv(1024).decode()

        print(cs_res)
        if (cs_res == "ok"):
            logged_in = True
            c_usname = c_login_usname[:]
            print("Here")
        else:
            program_phase = False

    # Request friend list from central server
    server_host_thread = Thread(
        target = server_host,
        args = (),
        daemon = True
    )
    server_host_thread.start()

    program_phase = False
    while not program_phase:
        continue

    get_friend_list_request(ccs_socket)

    upd_friend_status_request(ccs_socket)
  
    while req != "disconn":
        program_phase = False

        while not program_phase:
            continue

        print("Handling request: " + req)

        if req == "updfrstt":
            upd_friend_status_request(ccs_socket)
        elif req == "conn":
            cs_socket = connect_server_request(ccs_socket, req_args[0])
        elif req == "send":
            send_msg(cs_socket)
        elif req == "disconn":
            disconnect_server_request(ccs_socket)

        
"""
    Event handlers
"""

def grid_friend_list():
    global lst_btn_friends

    for btn in lst_btn_friends:
        btn.grid_forget
        lst_btn_friends.remove(btn)

    num_page = 0
    start_index = 0
    col = 0
    row = 0
    for i in range(start_index, start_index + 8):
        if i >= len(c_lst_friends):
            break

        status, username = c_lst_friends[i]
        if status != ["null", -1]:
            status = "Online"
        else:
            status = "Offline"

        btn_friend = tk.Button(
            fr_friends,
            height = 3,
            width = 16,
            text = username + "\n" + status,
            justify = "left",
            anchor = "w"
        )
        btn_friend.bind("<1>", btn_friend_handler)
        btn_friend.grid(
            row = row + 3,
            column = col + 1,
            rowspan = 2
        )

        lst_btn_friends.append(btn_friend)
        
        if col == 2:
            col = 0
            row += 2
        else:
            col += 1

def load_chat_promt(s_usname):
    global c_msg_histories
    global txt_chat_prompt

    for c_msg_history in c_msg_histories:
        name, hist = c_msg_history
        if s_usname == name:
            txt_chat_prompt.config(state = "normal")
            txt_chat_prompt.delete("1.0", tk.END)
            for msg in hist:
                txt_chat_prompt.insert(tk.END, msg + "\n")
            txt_chat_prompt.config(state = "disabled")
            
def btn_friend_handler(event):
    global req
    global req_args
    global program_phase
    global cs_socket

    c_req = "disconn"
    if not isinstance(cs_socket, int):
        cs_socket.send(c_req.encode())

    caller = event.widget
    s_usname = caller["text"].split("\n")[0]
    req = "conn"
    req_args = [s_usname]

    load_chat_promt(s_usname)
    program_phase = True

def btn_login_register_req_handler():
    fr_login.grid_forget()

    fr_reg.grid(
        row = 0,
        column = 0,
        rowspan = 5,
        columnspan = 5
    )

def btn_login_login_handler():
    global program_phase
    global c_login_usname
    global c_login_psword
    global cs_res
    global fr_login
    global fr_chatwindow
    global lbl_username
    global c_usname

    c_login_usname = ent_login_usname.get()
    c_login_psword = ent_login_psword.get()
    program_phase = True

    while (program_phase):
        continue
    
    if (cs_res == "ok"):
        c_login_usname = ""
        c_login_psword = ""
        cs_res = ""

        fr_login.grid_forget()
        fr_chatwindow.grid(
        row = 0,
        column = 0,
        rowspan = 15,
        columnspan = 10 
        )

        lbl_username.config(text = "Welcome, {}!".format(c_usname))
    else:
        c_login_usname = ""
        c_login_psword = ""
        cs_res = ""

def btn_reg_login_req_handler():
    fr_reg.grid_forget()

    fr_login.grid(
        row = 0,
        column = 0,
        rowspan = 4,
        columnspan = 4
    )

def btn_reg_register_handler():
    fr_reg.grid_forget()

    fr_login.grid(
        row = 0,
        column = 0,
        rowspan = 4,
        columnspan = 4
    )

def btn_friend_list_refresh_handler():
    global req
    global program_phase

    req = "updfrstt"
    program_phase = True

def btn_send_handler():
    global req
    global program_phase

    req = "send"
    program_phase = True

"""
    Thread defintions
"""
def server_request_handler(sc_conn, c_addr):
    global c_usname
    global connected_usname
    c_req = "null"

    while c_req != "disconn":
        print("Local server: Waiting for request ...")
        c_req = sc_conn.recv(1024).decode()
        sc_conn.send("ok".encode())

        if (c_req == "disconn"):
            sc_conn.close()

            for thread_info in lst_running_threads:
                thread, addr = thread_info

                if c_addr == addr:
                    lst_done_threads.append(thread_info)
                    lst_running_threads.remove(thread_info)

        elif c_req == "send":
            sender_usname = sc_conn.recv(1024).decode()
            sc_conn.send(c_usname.encode())
            msg = sc_conn.recv(1024).decode()
            sc_conn.send("ok".encode())

            flag = False
            for c_msg_history in c_msg_histories:
                if (sender_usname == c_msg_history[0]):
                    flag = True
                    c_msg_history[1].append(sender_usname + ": " + msg)
                    break
            if not flag:
                c_msg_histories.append([sender_usname, [sender_usname + ": " + msg]])
            
            if connected_usname == sender_usname:
                load_chat_promt(sender_usname)
    
# main()
"""
    Login page
"""
fr_login = tk.Frame(
    root,
    height = 100,
    width = 100
)
fr_login.grid(
    row = 0,
    column = 0,
    rowspan = 4,
    columnspan = 5
)

fr_login_lpad = tk.Frame(
    fr_login,
    height = 100,
    width = 10
)
fr_login_lpad.grid(
    row = 0,
    column = 0,
    rowspan = 4
)

fr_login_rpad = tk.Frame(
    fr_login,
    height = 100,
    width = 10
)
fr_login_rpad.grid(
    row = 0,
    column = 4,
    rowspan = 4
)

lbl_login = tk.Label(
    fr_login,
    height = 1,
    width = 10,
    text = "LOG IN",
    font = ("Arial", 15, "bold"),
    bg = "green"
)
lbl_login.grid(
    row = 0,
    column = 1,
    columnspan = 3
)

lbl_login_usname = tk.Label(
    fr_login,
    height = 1,
    width = 10,
    text = "Username:"
)
lbl_login_usname.grid(
    row = 1,
    column = 1
)

lbl_login_psword = tk.Label(
    fr_login,
    height = 1,
    width = 10,
    text = "Password:"
)
lbl_login_psword.grid(
    row = 2,
    column = 1
)

ent_login_usname = tk.Entry(
    fr_login,
    width = 26
)
ent_login_usname.grid(
    row = 1,
    column = 2,
    columnspan = 2
)

ent_login_psword = tk.Entry(
    fr_login,
    width = 26
)
ent_login_psword.grid(
    row = 2,
    column = 2,
    columnspan = 2
)

btn_login_login = tk.Button(
    fr_login,
    height = 1,
    width = 10,
    text = "Login",
    command = btn_login_login_handler
)
btn_login_login.grid(
    row = 3,
    column = 2
)

btn_login_register_req = tk.Button(
    fr_login,
    height = 1,
    width = 10,
    text = "Register",
    command = btn_login_register_req_handler
)
btn_login_register_req.grid(
    row = 3,
    column = 3
)

"""
    Register page
"""
fr_reg = tk.Frame(
    root,
    height = 100,
    width = 100
)

fr_reg_lpad = tk.Frame(
    fr_login,
    height = 100,
    width = 10
)
fr_reg_lpad.grid(
    row = 0,
    column = 0,
    rowspan = 5
)

fr_reg_rpad = tk.Frame(
    fr_reg,
    height = 100,
    width = 10
)
fr_reg_rpad.grid(
    row = 0,
    column = 5,
    rowspan = 5
)

lbl_reg = tk.Label(
    fr_reg,
    height = 1,
    width = 10,
    text = "REGISTER",
    font = ("Arial", 15, "bold"),
    bg = "green"
)
lbl_reg.grid(
    row = 0,
    column = 1,
    columnspan = 3
)

lbl_reg_usname = tk.Label(
    fr_reg,
    height = 1,
    width = 16,
    text = "Username:"
)
lbl_reg_usname.grid(
    row = 1,
    column = 1
)

lbl_reg_psword = tk.Label(
    fr_reg,
    height = 1,
    width = 16,
    text = "Password:"
)
lbl_reg_psword.grid(
    row = 2,
    column = 1
)

lbl_reg_confirm_psword = tk.Label(
    fr_reg,
    height = 1,
    width = 16,
    text = "Confirm password:"
)
lbl_reg_confirm_psword.grid(
    row = 3,
    column = 1
)

ent_reg_usname = tk.Entry(
    fr_reg,
    width = 26
)
ent_reg_usname.grid(
    row = 1,
    column = 2,
    columnspan = 2
)

ent_reg_psword = tk.Entry(
    fr_reg,
    width = 26
)
ent_reg_psword.grid(
    row = 2,
    column = 2,
    columnspan = 2
)

ent_reg_confirm_psword = tk.Entry(
    fr_reg,
    width = 26
)
ent_reg_confirm_psword.grid(
    row = 3,
    column = 2,
    columnspan = 2
)

btn_reg_login = tk.Button(
    fr_reg,
    height = 1,
    width = 10,
    text = "Login",
    command = btn_reg_login_req_handler
)
btn_reg_login.grid(
    row = 4,
    column = 2
)

btn_reg_register_req = tk.Button(
    fr_reg,
    height = 1,
    width = 10,
    text = "Register",
    command = btn_reg_register_handler
)
btn_reg_register_req.grid(
    row = 4,
    column = 3
)

"""
    Chat space
"""
fr_chatwindow = tk.Frame(
    root,
    height = 400,
    width = 500
)

fr_leftpad = tk.Frame(
    fr_chatwindow,
    height = 400,
    width = 10
)

fr_leftpad.grid(
    row = 0,
    column = 0,
    rowspan = 11
)

lbl_username = tk.Label(
    fr_chatwindow,
    height = 1,
    width = 51,
    text = "Username",
    justify = "left",
    anchor = "w"
)

lbl_username.grid(
    row = 0,
    column = 1,
    columnspan = 3
)

btn_logout = tk.Button(
    fr_chatwindow,
    height = 1,
    width = 51,
    text = "Log out"
)

btn_logout.grid(
    row = 1,
    column = 1,
    columnspan = 3
)

lbl_friendlist_header = tk.Label(
    fr_chatwindow,
    height = 1,
    width = 13,
    padx = 10,
    text = "Friend list",
    font = ("Arial", 20, "bold"),
    anchor = "w",
    bg = "green"
)

lbl_friendlist_header.grid(
    row = 2,
    column = 1,
    columnspan = 2
)

fr_friends = tk.Frame(
    fr_chatwindow,
    height = 100,
    width = 100
)

fr_friends.grid(
    row = 3,
    column = 1,
    rowspan = 6,
    columnspan = 3
)

lst_btn_friends = []
grid_friend_list()

btn_friend_list_refresh = tk.Button(
    fr_chatwindow,
    height = 1,
    width = 12,
    text = "Refresh",
    command = btn_friend_list_refresh_handler
)
btn_friend_list_refresh.grid(
    row = 2,
    column = 3
)

btn_friends_next = tk.Button(
    fr_chatwindow,
    height = 1,
    width = 16,
    text = "Next"
)

btn_friends_next.grid(
    row = 9,
    column = 2,
)

btn_friends_prev = tk.Button(
    fr_chatwindow,
    height = 1,
    width = 16,
    text = "Previous"
)

btn_friends_prev.grid(
    row = 9,
    column = 1,
)

btn_friends_first = tk.Button(
    fr_chatwindow,
    height = 1,
    width = 16,
    text = "First"
)

btn_friends_first.grid(
    row = 9,
    column = 3,
)

fr_footer = tk.Frame(
    fr_chatwindow,
    height = 30,
    width = 500
)

fr_footer.grid(
    row = 10,
    column = 1,
    columnspan = 8
)

fr_middlepad = tk.Frame(
    fr_chatwindow,
    height = 400,
    width = 20
)

fr_middlepad.grid(
    row = 0,
    column = 4,
    rowspan = 11
)

lbl_chat_usname = tk.Label(
    fr_chatwindow,
    height = 1,
    width = 25,
    padx = 30,
    text = "Name",
    font = ("Arial", 15, "bold"),
    justify = "left",
    anchor = "nw"
)

lbl_chat_usname.grid(
    row = 0,
    column = 5,
    columnspan = 3
)

lbl_chat_detail = tk.Label(
    fr_chatwindow,
    height = 1,
    width = 43,
    padx = 30,
    text = "Status",
    justify = "left",
    anchor = "nw",
)

lbl_chat_detail.grid(
    row = 1,
    column = 5,
    columnspan = 3
)

txt_chat_prompt = tk.Text(
    fr_chatwindow,
    height = 14,
    width = 51,
    state = "disabled"
)

txt_chat_prompt.grid(
    row = 2,
    column = 5,
    rowspan = 6,
    columnspan = 3
)

btn_attach_file = tk.Button(
    fr_chatwindow,
    height = 1,
    width = 15,
    text = "Attach file"
)

btn_attach_file.grid(
    row = 8,
    column = 5
)

lbl_attached_file = tk.Label(
    fr_chatwindow,
    height = 1,
    width = 39,
    padx = 10,
    text = "Attached file",
    justify = "left",
    anchor = "nw"
)

lbl_attached_file.grid(
    row = 8,
    column = 6,
    columnspan = 2
)

txt_text_prompt = tk.Text(
    fr_chatwindow,
    height = 2,
    width = 36,
)

txt_text_prompt.grid(
    row = 9,
    column = 5,
    columnspan = 2
)

btn_send = tk.Button(
    fr_chatwindow,
    height = 1,
    width = 15,
    text = "Send",
    command = btn_send_handler
)

btn_send.grid(
    row = 9,
    column = 7
)

program_thread = Thread(
    target = program
)

program_thread.start()

root.mainloop()

program_thread.join()
