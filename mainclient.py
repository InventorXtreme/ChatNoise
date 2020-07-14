import requests
import threading
from tkinter import *
import time
import pickle
import tkinter
from tkinter import messagebox


global updategood
updategood = True
from tkinter import simpledialog
import os
import webbrowser

clientversion = "- 0.2.9a"
import urllib.request
from PIL import Image, ImageTk

root = Tk()
from sframe import ScrollFrame, Example

global user, server, port
try:
    config = pickle.load(open("config.p", "rb"))
    user = config["username"]
    server = config["server"]
    port = config["port"]
    print("config loaded")
    print(user)
except:
    print("CONFIG ERROR: SETTING UP")
    namesetup = input("NAME: ")
    serversetup = input("IP: ")
    portsetupIN = input("port: ")
    portsetup = ":" + portsetupIN
    config = {"username": "DEFULT USER", "server": "127.0.0.1", "port": ":69"}
    config["server"] = serversetup
    config["port"] = portsetup
    config["username"] = namesetup
    pickle.dump(config, open("config.p", "wb+"))
    config = pickle.load(open("config.p", "rb"))
    user = config["username"]
    server = config["server"]
    port = config["port"]
    print("config loaded")
    print(user)


def changename():
    global user, server, port
    print("CONFIG NAME SETTUP STARTED")
    namesetup = simpledialog.askstring("Chat Noise -> Settings -> Username", "Input New Username:")
    config = pickle.load(open("config.p", "rb"))

    config["username"] = namesetup

    pickle.dump(config, open("config.p", "wb+"))
    config = pickle.load(open("config.p", "rb"))
    user = config["username"]
    server = config["server"]
    port = config["port"]
    print("config loaded")
    print(user)


def changeserver():
    global user, server, port
    print("CONFIG NAME SETTUP STARTED")
    namesetup = simpledialog.askstring("Chat Noise -> Settings -> Server", "Input New Server:")
    config = pickle.load(open("config.p", "rb"))

    config["server"] = namesetup

    pickle.dump(config, open("config.p", "wb+"))
    config = pickle.load(open("config.p", "rb"))
    user = config["username"]
    server = config["server"]
    port = config["port"]
    print("config loaded")
    print(user)


def changeport():
    global user, server, port
    print("CONFIG NAME SETTUP STARTED")

    namesetup = simpledialog.askstring("Chat Noise -> Settings -> Port", "Input New Port:")
    config = pickle.load(open("config.p", "rb"))

    config["port"] = ":" + namesetup

    pickle.dump(config, open("config.p", "wb+"))
    config = pickle.load(open("config.p", "rb"))
    user = config["username"]
    server = config["server"]
    port = config["port"]
    print("config loaded")
    print(user)


def loadimagebrowser():
    print("loaded")
    base64_img = simpledialog.askstring("Chat Noise -> B64 Image Decoder", "Input Image Data to Decode")
    url = "http://" + server + port + "/image/" + base64_img
    webbrowser.open(url, new=2)


def loadimage():
    print("loaded")
    base64_img = simpledialog.askstring("Chat Noise -> B64 Image Decoder", "Input Image Data to Decode")
    url = "http://" + server + port + "/image/" + base64_img
    # webbrowser.open(url,new=2)

    try:
        urllib.request.urlretrieve(url, "./cimg/cashedimage")
        popup = tkinter.Toplevel(root)
        img = Image.open("./cimg/cashedimage")
        tatras = ImageTk.PhotoImage(img)

        label = Label(popup, image=tatras)
        label.pack()
        popup.mainloop()
    except FileNotFoundError:
        os.mkdir("cimg")
        urllib.request.urlretrieve(url, "./cimg/cashedimage")
        popup = tkinter.Toplevel(root)
        img = Image.open("./cimg/cashedimage")
        tatras = ImageTk.PhotoImage(img)

        label = Label(popup, image=tatras)
        label.pack()
        popup.mainloop()


global img_data_dict
img_data_dict = {}

global imgpopup
imgpopup = tkinter.Toplevel(root)
imgpopup.title("5 most recent images")
global scrollFrame

global img_names
img_names = []
global loadimagelist_count
loadimagelist_count = 0


def loadimagelist(img):
    global loadimagelist_count
    global scrollFrame
    global img_data_dict
    global imgpopup
    print("loaded")
    loadimagelist_count += 1
    # base64_img = simpledialog.askstring("Chat Noise -> B64 Image Decoder", "Input Image Data to Decode")
    url = "http://" + server + port + "/image/" + img
    # webbrowser.open(url,new=2)

    try:
        urllib.request.urlretrieve(url, "./cimg/cashedimage")
        imgd = Image.open("./cimg/cashedimage")
        img_data_dict[loadimagelist_count] = ImageTk.PhotoImage(imgd)

        label = Label(scrollFrame.viewPort, image=img_data_dict[loadimagelist_count])

        label.pack(side=TOP)
        return label

    except FileNotFoundError:
        os.mkdir("cimg")
        urllib.request.urlretrieve(url, "./cimg/cashedimage")
        imgd = Image.open("./cimg/cashedimage")
        img_data_dict[loadimagelist_count] = ImageTk.PhotoImage(imgd)

        label = Label(scrollFrame.viewPort, image=img_data_dict[loadimagelist_count])
        label.pack(side=TOP)
        return label


def uploadimage():
    print("encoded")
    url = "http://" + server + port + "/upimage"
    webbrowser.open(url, new=2)


def all_children(window):
    _list = window.winfo_children()

    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())

    return _list


def openfile():
    print("openfiled")
    os.system("out.txt")


def sync():
    print("sync")
    send()


def send_clip():
    print("send_clip")
    send(root.clipboard_get())


def getid():
    servboi = "http://" + server + port + "/messageid/"
    out = requests.get(servboi)
    return out.text


def send(senddata):
    print("sendt")
    try:
        outline = user + ": " + senddata
    except TypeError:
        messagebox.showerror("Chat Noise Config Error", "You must have a username to send a message")
    servboi = "http://" + server + port + "?send="
    toadd = getid()
    added1 = int(toadd)
    added2 = added1 + 1
    addedout = str(added2)
    out = servboi + outline + "&id=" + addedout
    temp = requests.get(out)


def sendnbs(senddata):
    print("sendt")
    try:
        outline = senddata
    except TypeError:
        messagebox.showerror("Chat Noise Config Error", "You must have a username to send a message")
    servboi = "http://" + server + port + "?send="
    toadd = getid()
    added1 = int(toadd)
    added2 = added1 + 1
    addedout = str(added2)
    out = servboi + outline + "&id=" + addedout
    temp = requests.get(out)


def setupdate():
    print("what does this do")
    global updategood
    updategood = not updategood


def sendread(a):
    print("read")
    try:
        send(chatbox.get())
        chatbox.delete(0, END)
    except requests.exceptions.ConnectionError:
        tkinter.messagebox.showerror(title="NetError", message="Connection Error sending data to server")


def sendreadb():
    sendread("f")


def about():
    print("abouted")
    try:
        url = "http://" + server + port + "/ver"
        temp = requests.get(url)
        serverversion = temp.text
    except:
        serverversion = "Error connecting to server"

    messagebox.showinfo(title="About", message="ChatNoise -> A chat client/protocol for the people\n"
                                               "Developed By: Alex Moening\n"
                                               "Client Version " + clientversion + ""
                                                                                   " using Tkinter GUI\n"
                                                                                   "Server Version: " + serverversion)


def imglistpopup():
    global imgpopup
    global img_data_dict
    global img_list
    widget_list = all_children(imgpopup)
    for item in widget_list:
        item.pack_forget()


global ref_count
ref_count = 0


def refresh(h):
    global ref_count
    print("refeshed")
    while True:
        if updategood != False:
            x = get_data()
            if ref_count % 5 == 0:
                try:
                    imgextract()
                except tkinter.TclError:
                    pass

            text.delete('1.0', END)
            text.insert(END, x)
            text.see(END)
            ref_count += 1
            time.sleep(3)


def img_sause():
    base64_img = simpledialog.askstring("Chat Noise -> B64 Image Decoder", "Input Image to send")
    out = "img|" + base64_img
    sendnbs(out)


root.configure(background='grey10')
Title = "Python Chat Noise Client " + clientversion
root.title(Title)
root.bind('<Return>', sendread)
text = Text(root, width=80, height=20, bg="grey10", fg="white")
text.pack()
chatboxframe = Frame(root, bg="grey10")
chatboxframe.pack()
chatbox = Entry(chatboxframe, width=100, bg="grey10", fg="white")
chatbox.pack(side=LEFT)
sendb = Button(chatboxframe, command=sendreadb, text="send", bg="grey10", fg="red3")
sendb.pack(side=RIGHT)

menubar = Menu(root)

Plugs = Menu(root)

settingsmenu = Menu(root)


settingsmenu.add_command(label="Change Username", command=changename)
settingsmenu.add_command(label="Change Server", command=changeserver)
settingsmenu.add_command(label="Change Port", command=changeport)

codemenu = Menu(root)


def imglistpopup_caller():
    global imgpopup
    imgpopup = tkinter.Toplevel(root)
    imglistpopup()


codemenu.add_command(label="Upload", command=uploadimage)
codemenu.add_command(label="Open", command=loadimage)
codemenu.add_command(label="Open in Browser", command=loadimagebrowser)
codemenu.add_command(label="Imagelist", command=imglistpopup_caller)
codemenu.add_command(label="SAUSE", command=img_sause)

FileMenu = Menu(menubar)

# FileMenu.add_command(label="Settings",command=settings)

FileMenu.add_command(label="Enable/Disable Refresh", command=setupdate)
FileMenu.add_command(label="Send Clipboard", command=send_clip)
FileMenu.add_command(label="About", command=about)
menubar.add_cascade(label="File", menu=FileMenu)
menubar.add_cascade(label="Encode/Decode Images", menu=codemenu)
menubar.add_cascade(label="Settings", menu=settingsmenu)
root.config(menu=menubar)


def get_data():
    print("display")
    iservboi = "http://" + server + port + "?get"
    try:
        down = requests.get(iservboi)
    except requests.exceptions.ConnectionError:
        return "Error Connecting to server"
    x = down.text
    with open("chatlogclient.txt", "w+") as file:
        file.write(x)
    with open("chatlogclient.txt", 'r') as fin:
        return fin.read()


global img_list
img_list = {}


def imgextract():
    imglistpopup()
    global img_list
    global img_names
    global imgpopup
    global scrollFrame
    img_list.clear()
    cnt = 1
    cntimg = 0
    iservboi = "http://" + server + port + "?get"
    scrollFrame = ScrollFrame(imgpopup)  # add a new scrollable frame.

    try:
        down = requests.get(iservboi)
    except requests.exceptions.ConnectionError:
        return "Error Connecting to server"
    x = down.text
    with open("chatlogclienti.txt", "w+") as file:
        file.write(x)
    with open("chatlogclienti.txt", 'r') as fin:
        filestring = fin.read()
        linelist = filestring.split("\n")
        linelist.reverse()

        while True:
            goto = False
            try:
                line = linelist[cnt]
            except IndexError:
                break

            command = line.split("|")
            if command[0] == "img" and cntimg < 5:
                img_list[command[1]] = loadimagelist(command[1])
                img_names.append(command[1])
                cntimg += 1

            cnt += 1
    scrollFrame.pack(side="top", fill="both", expand=True)

GuiLoop = threading.Thread(target=refresh, args=(1,), daemon=True)
GuiLoop.start()

root.mainloop()
