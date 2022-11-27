import tkinter as tk

root = tk.Tk()

lst_friends = [(False, "tokarinrika"),
               (True, "HarryHaha"), 
               (True, "Anonymous"),
               (False, "Rabbit"),
               (True, "Winter-oneesan")]

fr_leftpad = tk.Frame(
    root,
    height = 400,
    width = 10
)

fr_leftpad.grid(
    row = 0,
    column = 0,
    rowspan = 11
)

lbl_username = tk.Label(
    root,
    height = 1,
    width = 51,
    text = "Username"
)

lbl_username.grid(
    row = 0,
    column = 1,
    columnspan = 3
)

btn_logout = tk.Button(
    root,
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
    root,
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
    root,
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
num_page = 0
start_index = 0
col = 0
row = 0
for i in range(start_index, start_index + 8):
    if i >= len(lst_friends):
        break

    status, username = lst_friends[i]
    if status:
        status = "Online"
    else:
        status = "Offline"

    btn_friend = tk.Button(
        fr_friends,
        height = 3,
        width = 16,
        text = username + "\n" + status,
        justify = "left"
    )

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

btn_friends_next = tk.Button(
    root,
    height = 1,
    width = 16,
    text = "Next"
)

btn_friends_next.grid(
    row = 9,
    column = 2,
)

btn_friends_prev = tk.Button(
    root,
    height = 1,
    width = 16,
    text = "Previous"
)

btn_friends_prev.grid(
    row = 9,
    column = 1,
)

btn_friends_first = tk.Button(
    root,
    height = 1,
    width = 16,
    text = "First"
)

btn_friends_first.grid(
    row = 9,
    column = 3,
)

fr_footer = tk.Frame(
    root,
    height = 30,
    width = 500
)

fr_footer.grid(
    row = 10,
    column = 1,
    columnspan = 8
)

fr_middlepad = tk.Frame(
    root,
    height = 400,
    width = 20
)

fr_middlepad.grid(
    row = 0,
    column = 4,
    rowspan = 11
)

lbl_chat_detail = tk.Label(
    root,
    height = 2,
    width = 25,
    padx = 50,
    text = "Name\nDetail",
    font = ("Arial", 15, "bold"),
    justify = "left",
    anchor = "nw"
)

lbl_chat_detail.grid(
    row = 0,
    column = 5,
    rowspan = 2,
    columnspan = 3
)

txt_chat_prompt = tk.Text(
    root,
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
    root,
    height = 1,
    width = 15,
    text = "Attach file"
)

btn_attach_file.grid(
    row = 8,
    column = 5
)

lbl_attached_file = tk.Label(
    root,
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
    root,
    height = 2,
    width = 36,
)

txt_text_prompt.grid(
    row = 9,
    column = 5,
    columnspan = 2
)

btn_send = tk.Button(
    root,
    height = 1,
    width = 15,
    text = "Send"
)

btn_send.grid(
    row = 9,
    column = 7
)

root.mainloop()
