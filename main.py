import socket
import tkinter
import tkinter.messagebox
from tkinter import *
import ipaddress

host = ""
ports = []


def knock():
    try:
        if ipaddress.ip_address(ipEntry.get()):
            for port in ports:
                print(f"[+] Knocking on port {host}:{port}")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0)
                sock.connect_ex((host, port))
                sock.close()
            tkinter.messagebox.showinfo("Ok!", "Knocking!")
    except ValueError:
        tkinter.messagebox.showerror("Error!", "Invalid IP Address!")


def add_port():
    try:
        if isinstance(int(entry_box.get()), int):
            listbox.insert(listbox.size(), entry_box.get())
            ports.append(int(entry_box.get()))
            entry_box.delete(0, END)
    except ValueError:
        tkinter.messagebox.showerror("Error!", "Invalid Port!")
        entry_box.delete(0, END)


def delete():
    listbox.delete(tkinter.ANCHOR)
    content = listbox.get(0, END)
    ports.clear()
    for i in range(len(content)):
        ports.append(int(content[i]))
        print(ports)


window = Tk()
window.geometry("250x300")
window.title("Port Knocker")
window.resizable(False, False)


text = Label(window, text="IP Address:", width=20, anchor="nw")
text.pack()

ipEntry = Entry(window)
ipEntry.pack()


emptyLabel1 = Label(window, height=1)
emptyLabel1.pack()


text2 = Label(window, text="Ports:", width=20, anchor="nw")
text2.pack()

listbox = Listbox(window, width=20, height=5)
listbox.pack()

emptyLabel2 = Label(window, height=1)
emptyLabel2.pack()

emptyLabel3 = Label(window, text="Add Port:", width=20, anchor="nw")
emptyLabel3.pack()

entry_box = Entry(window, width=20)
entry_box.pack()


button = Button(window, text="Add Port", command=add_port)
button.pack()


button2 = Button(window, text="Knock", command=knock)
button2.pack()

button5 = Button(window, text="Delete", command=delete, anchor="center", width=5)
button5.place(x="200", y="100")

window.mainloop()


