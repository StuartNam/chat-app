import tkinter as tk

def onClick(event):
    caller = event.widget
    caller.config(text = "You suck")

root = tk.Tk()

btn1 = tk.Button(
    root,
    text = "Btn1"
)
btn1.pack()
btn1.bind("<1>", onClick)

root.mainloop()