import socket
import tkinter
import tkinter.messagebox
from tkinter import *
import ipaddress
import os
import json
import select

ports = []

if not os.path.isfile("profiles.json"):
    with open('profiles.json', 'w') as f:
        f.write("{}")


class MainScreen:
    def __init__(self, root):
        self.root = root
        self.frame = tkinter.Frame(self.root)
        self.frame.pack()
        self.app = App(self.root, self)

        self.label = Label(self.frame, text="Port Knocker", anchor="nw")
        self.label.pack()

        self.label2 = Label(self.frame, text="by Krasimir Lukanov for ToolDomains")
        self.label2.pack()

        self.label3 = Label(self.frame, text="Saved Profiles", anchor="nw")
        self.label3.pack()

        self.label.config(font=("Ariel", 15), anchor="nw")
        self.label2.config(font=("Ariel", 10), anchor="nw")
        self.label3.config(font=("Ariel", 10), anchor="nw")

        self.scrollbar = Scrollbar(self.frame)
        self.listbox = Listbox(self.frame, yscrollcommand=self.scrollbar.set)

        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack()

        self.new_profile_btn = Button(self.frame, text="New Profile", width=10, height=2,
                                      command=self.port_knock_switch)
        self.open_profile_btn = Button(self.frame, text="Open Profile", width=10, height=2, command=self.open_profile)
        self.del_profile_btn = Button(self.frame, text="Delete Profile", width=10, height=2, command=self.del_profile)

        self.knock_btn = Button(self.frame, text="Knock", width=10, height=2, command=self.knock)

        self.new_profile_btn.pack()
        self.open_profile_btn.pack()
        self.del_profile_btn.pack()
        self.knock_btn.pack()

        self.load_profile_names()

    def start_page(self):
        self.frame.pack()

    def port_knock_switch(self):
        self.frame.pack_forget()
        self.app.start_page()

    def open_profile(self):
        self.app.edit_mode = True
        text = None
        idxs = self.listbox.curselection()

        if not idxs:
            tkinter.messagebox.showerror("Error!", "Please select a profile and try again!")
        for pos in idxs:
            text = self.listbox.get(pos)
            print(text)

        with open('profiles.json', 'r') as f:
            profiles = json.load(f)

            self.app.ipEntry.insert(0, profiles[text]["host"])
            ports.clear()
            for i in profiles[text]['ports']:
                self.app.listbox.insert(END, str(i))
                ports.append(int(i))
            self.app.profile_name.insert(0, text)
            self.app.current_profile = text
        self.port_knock_switch()

    def del_profile(self):
        text = None

        idxs = self.listbox.curselection()

        if not idxs:
            tkinter.messagebox.showerror("Error!", "Please select a profile and try again!")

        for pos in idxs:
            text = self.listbox.get(pos)
            self.listbox.delete(pos)

        with open('profiles.json', 'r') as f:
            profiles = json.load(f)

            profiles.pop(text)

        with open('profiles.json', 'w') as f:
            json.dump(profiles, f)

    def load_profile_names(self):
        with open('profiles.json', 'r') as f:
            profiles = json.load(f)

            for i in profiles:
                self.listbox.insert(END, str(i))

    def knock(self):
        print("Knocking")
        idxs = self.listbox.curselection()
        if not idxs:
            tkinter.messagebox.showerror("Error!", "Please select a profile and try again!")
        for pos in idxs:
            text = self.listbox.get(pos)

            with open('profiles.json', 'r') as f:
                profiles = json.load(f)

                ip = profiles[text]["host"]
                ports.clear()
                for port in profiles[text]["ports"]:
                    ports.append(port)

            for port in ports:
                print(port)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setblocking(False)
                sock.settimeout(0.2)

                sock.connect_ex((ip, port))
                select.select([sock], [sock], [sock], 0)

                sock.close()
            tkinter.messagebox.showinfo("Ok!", "Knocking!")


class App:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.frame = tkinter.Frame(self.root)
        self.edit_mode = False
        self.current_profile = ""
        self.text = Label(self.frame, text="IP Address:", width=20, anchor="nw")
        self.text.pack()

        self.ipEntry = Entry(self.frame)
        self.ipEntry.pack()

        self.emptyLabel1 = Label(self.frame, height=1)
        self.emptyLabel1.pack()

        self.text2 = Label(self.frame, text="Ports:", width=20, anchor="nw")
        self.text2.pack()

        self.listbox = Listbox(self.frame, width=20, height=5)
        self.listbox.pack()

        self.emptyLabel2 = Label(self.frame, height=1)
        self.emptyLabel2.pack()

        self.emptyLabel3 = Label(self.frame, text="Add Port:", width=20, anchor="nw")
        self.emptyLabel3.pack()

        self.port = Entry(self.frame, width=20)
        self.port.pack()

        self.emptyLabel4 = Label(self.frame, height=1)
        self.emptyLabel4.pack()

        self.text3 = Label(self.frame, text="Profile Name:", width=20, anchor="nw")
        self.text3.pack()

        self.profile_name = Entry(self.frame)
        self.profile_name.pack()

        self.button = Button(self.frame, text="Add Port", command=self.add_port, width=10)
        self.button.pack()

        self.button2 = Button(self.frame, text="Knock", command=self.knock, width=10)
        self.button2.pack()

        self.button3 = Button(self.frame, text="Delete", command=self.delete_port, anchor="center", width=10)
        self.button3.pack()

        self.save = Button(self.frame, text="Save", command=self.save_profile, width=10)
        self.save.pack()

        self.back = Button(self.frame, text="Go Back", command=self.main_screen_switch, anchor="center", width=10)
        self.back.pack()

    def start_page(self):
        self.frame.pack()

    def main_screen_switch(self):
        self.edit_mode = False
        self.frame.pack_forget()
        self.app.start_page()
        self.ipEntry.delete(0, END)
        self.port.delete(0, END)
        self.listbox.delete(0, END)
        self.profile_name.delete(0, END)

    def knock(self):
        try:
            if ipaddress.ip_address(self.ipEntry.get()):
                for port in ports:
                    print(port)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.setblocking(False)
                    sock.settimeout(0.2)

                    sock.connect_ex((self.ipEntry.get(), port))
                    select.select([sock], [sock], [sock], 0)

                    sock.close()
                tkinter.messagebox.showinfo("Ok!", "Knocking!")
        except ValueError:
            tkinter.messagebox.showerror("Error!", "Invalid IP Address!")

    def add_port(self):
        try:
            self.listbox.insert(self.listbox.size(), self.port.get())
            ports.append(int(self.port.get()))
            self.port.delete(0, END)
        except ValueError:
            tkinter.messagebox.showerror("Error!", "Invalid Port!")
            self.port.delete(0, END)

    def delete_port(self):
        self.listbox.delete(tkinter.ANCHOR)
        content = self.listbox.get(0, END)
        ports.clear()
        for i in range(len(content)):
            ports.append(int(content[i]))
            print(ports)

    def save_profile(self):
        if self.ipEntry.get():
            if self.profile_name.get():
                if len(ports) > 0:
                    self.save_file()
                    self.main_screen_switch()
                else:
                    tkinter.messagebox.showerror("Error!", "Please provide some ports!")
            else:
                tkinter.messagebox.showerror("Error!", "Please provide profile name!")
        else:
            tkinter.messagebox.showerror("Error!", "Please provide an IP Address!!")

    def save_file(self):
        if not self.edit_mode:
            if self.check_if_profile_exists(self.profile_name.get()):
                with open('profiles.json', 'r') as f:
                    profiles = json.load(f)

                    profiles[self.profile_name.get()] = {}
                    profiles[self.profile_name.get()]["host"] = self.ipEntry.get()
                    profiles[self.profile_name.get()]["ports"] = ports

                with open('profiles.json', 'w') as f:
                    json.dump(profiles, f)

                self.update_profiles(self.profile_name.get())
            else:
                tkinter.messagebox.showerror("Error!", "A profile with that name already exists!")
        else:
            with open('profiles.json', 'r') as f:
                profiles = json.load(f)

                profiles[self.profile_name.get()] = profiles.pop(self.current_profile)
                profiles[self.profile_name.get()]['host'] = self.ipEntry.get()
                profiles[self.profile_name.get()]['ports'] = ports

            with open('profiles.json', 'w') as f:
                json.dump(profiles, f)

            idx = self.app.listbox.get(0, END).index(self.current_profile)
            self.app.listbox.delete(idx)
            self.app.listbox.insert(idx, self.profile_name.get())
            self.main_screen_switch()
            self.edit_mode = False

    def update_profiles(self, profile_name):
        self.app.listbox.insert(END, profile_name)

    @staticmethod
    def check_if_profile_exists(profile_name):
        with open('profiles.json', 'r') as f:
            profiles = json.load(f)

            for i in profiles:
                if i == profile_name:
                    return False
            return True


window = Tk()
window.title("Port Knocker")
window.geometry("400x450")
window.resizable(False, False)
app = MainScreen(window)
window.mainloop()
