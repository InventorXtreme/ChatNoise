import requests
from ctypes import windll
import threading
from tkinter import *
import time
import pickle
import tkinter
from tkinter import messagebox
import tkinter as tk
import imghdr
import ctypes
from tkinter import simpledialog
import os
import webbrowser
import urllib.request
from tkinter import filedialog
from PIL import Image, ImageTk
from elevate import elevate

windll.shcore.SetProcessDpiAwareness(1)
#elevate()           #reeeee this makes me want to die
#use git pull to update repo
clientversion = "- 0.9.5" #Todo - change to 0.9.5
from sframe import ScrollFrame

global updategood
updategood = True



global user, server, port
try:
    config = pickle.load(open("files/config.p", "rb"))
    user = config["username"]
    server = config["server"]
    port = config["port"]
    print("config loaded")
    print(user)
except:
    os.mkdir("files")
    print("CONFIG ERROR: SETTING UP")
    namesetup = input("NAME: ")
    serversetup = input("IP: ")
    portsetupIN = input("port: ")
    portsetup = ":" + portsetupIN
    config = {"username": "DEFULT USER", "server": "127.0.0.1", "port": ":69"}
    config["server"] = serversetup
    config["port"] = portsetup
    config["username"] = namesetup
    pickle.dump(config, open("files/config.p", "wb+"))
    config = pickle.load(open("files/config.p", "rb"))
    user = config["username"]
    server = config["server"]
    port = config["port"]
    print("config loaded")
    print(user)

class CustomText(Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = IntVar()
        indexlist = []
        while True:

            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")


def changename():
    global user, server, port
    print("CONFIG NAME SETTUP STARTED")
    namesetup = simpledialog.askstring("Chat Noise -> Settings -> Username", "Input New Username:")
    config = pickle.load(open("files/config.p", "rb"))

    config["username"] = namesetup

    pickle.dump(config, open("files/config.p", "wb+"))
    config = pickle.load(open("files/config.p", "rb"))
    user = config["username"]
    server = config["server"]
    port = config["port"]
    print("config loaded")
    print(user)


def changeserver():
    global user, server, port
    print("CONFIG NAME SETTUP STARTED")
    namesetup = simpledialog.askstring("Chat Noise -> Settings -> Server", "Input New Server:")
    config = pickle.load(open("files/config.p", "rb"))

    config["server"] = namesetup

    pickle.dump(config, open("files/config.p", "wb+"))
    config = pickle.load(open("files/config.p", "rb"))
    user = config["username"]
    server = config["server"]
    port = config["port"]
    print("config loaded")
    print(user)

def embedup():
    print("embedup called")
    filename = filedialog.askopenfilename(filetypes=(("Images", "*.jpg"),("Images","*.png"),("Images","*.jpeg"),("Images","*.gif")))
    url = "http://" + server + port + "/upimage/"
    try:
        with open(filename,'rb') as filedata:
            request = requests.post(url,files={'file':filedata})
            outname = os.path.basename(filedata.name)
            img_post(outname)
    except:
        print("embedup error")
        pass
def changeport():
    global user, server, port
    print("CONFIG NAME SETTUP STARTED")

    namesetup = simpledialog.askstring("Chat Noise -> Settings -> Port", "Input New Port:")
    config = pickle.load(open("files/config.p", "rb"))

    config["port"] = ":" + namesetup

    pickle.dump(config, open("files/config.p", "wb+"))
    config = pickle.load(open("files/config.p", "rb"))
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

class AnimatedGIF(Label, object):
    def __init__(self, master, path, forever=True):
        self._master = master
        self._loc = 0
        self._forever = forever

        self._is_running = False

        im = Image.open(path)
        self._frames = []
        i = 0
        try:
            while True:
                photoframe = ImageTk.PhotoImage(im.copy().convert('RGBA'))
                self._frames.append(photoframe)

                i += 1
                im.seek(i)
        except EOFError:
            pass

        self._last_index = len(self._frames) - 1

        try:
            self._delay = im.info['duration']
        except:
            self._delay = 100

        self._callback_id = None

        super(AnimatedGIF, self).__init__(master, image=self._frames[0])

    def start_animation(self, frame=None):
        if self._is_running: return

        if frame is not None:
            self._loc = 0
            self.configure(image=self._frames[frame])

        self._master.after(self._delay, self._animate_GIF)
        self._is_running = True

    def stop_animation(self):
        if not self._is_running: return

        if self._callback_id is not None:
            self.after_cancel(self._callback_id)
            self._callback_id = None

        self._is_running = False

    def _animate_GIF(self):
        self._loc += 1
        self.configure(image=self._frames[self._loc])

        if self._loc == self._last_index:
            if self._forever:
                self._loc = 0
                self._callback_id = self._master.after(self._delay, self._animate_GIF)
            else:
                self._callback_id = None
                self._is_running = False
        else:
            self._callback_id = self._master.after(self._delay, self._animate_GIF)

    def pack(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).pack(**kwargs)

    def grid(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).grid(**kwargs)

    def place(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).place(**kwargs)

    def pack_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).pack_forget(**kwargs)

    def grid_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).grid_forget(**kwargs)

    def place_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).place_forget(**kwargs)


def loadimage():
    base64_img = simpledialog.askstring("Chat Noise -> B64 Image Decoder", "Input Image Data to Decode")
    print("loaded")
    url = "http://" + server + port + "/image/" + base64_img
    # webbrowser.open(url,new=2)

    try:
        urllib.request.urlretrieve(url, "./cimg/cashedimage")
        popup = tkinter.Toplevel(root)
        img = Image.open("./cimg/cashedimage")
        width, height = img.size


        tatras = ImageTk.PhotoImage(img)

        #label = Label(popup, image=tatras)
        #label.pack(expand=True,fill=BOTH)
        packboi = ResizeFrame(popup,picimg=img)
        packboi.pack(fill=BOTH, expand=YES)
        popup.mainloop()

    except FileNotFoundError:
        os.mkdir("cimg")
        urllib.request.urlretrieve(url, "./cimg/cashedimage")
        popup = tkinter.Toplevel(root)
        img = Image.open("./cimg/cashedimage")
        width, height = img.size

        tatras = ImageTk.PhotoImage(img)

        # label = Label(popup, image=tatras)
        # label.pack(expand=True,fill=BOTH)
        packboi = ResizeFrame(popup, picimg=img)
        packboi.pack(fill=BOTH, expand=YES)
        popup.mainloop()

class ResizeFrame(Frame):
    def __init__(self, master, *pargs,picimg):
        Frame.__init__(self, master, *pargs)



        self.image = picimg
        self.img_copy= self.image.copy()


        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=True)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self,event):
        #TODO: SCALE IMAGE with ratio

        #get scale factor for chosen width or hieght somehow
        #Multiply other value by scale factor
        new_width = event.width -4
        new_height = event.height -4

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)


def openinpreview(base64_img):
    print("loaded")
    url = "http://" + server + port + "/image/" + base64_img
    # webbrowser.open(url,new=2)

    try:
        urllib.request.urlretrieve(url, "./cimg/cashedimage")
        popup = tkinter.Toplevel(root)
        popup.title(base64_img)
        img = Image.open("./cimg/cashedimage")
        width, height = img.size


        tatras = ImageTk.PhotoImage(img)

        #label = Label(popup, image=tatras)
        #label.pack(expand=True,fill=BOTH)
        packboi = ResizeFrame(popup,picimg=img)
        packboi.pack(fill=BOTH, expand=YES)
        popup.mainloop()

    except FileNotFoundError:
        os.mkdir("cimg")
        urllib.request.urlretrieve(url, "./cimg/cashedimage")
        popup = tkinter.Toplevel(root)
        popup.title(base64_img)
        img = Image.open("./cimg/cashedimage")
        width, height = img.size

        tatras = ImageTk.PhotoImage(img)

        # label = Label(popup, image=tatras)
        # label.pack(expand=True,fill=BOTH)
        packboi = ResizeFrame(popup, picimg=img)
        packboi.pack(fill=BOTH, expand=YES)
        popup.mainloop()

global img_data_dict
img_data_dict = {}

global img_dict
img_dict = {}
#global imgpopup
#imgpopup = tkinter.Toplevel(root)
#imgpopup.title("5 most recent images")
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
    global img_dict
    print("loaded")
    loadimagelist_count += 1
    # base64_img = simpledialog.askstring("Chat Noise -> B64 Image Decoder", "Input Image Data to Decode")
    url = "http://" + server + port + "/image/" + img
    # webbrowser.open(url,new=2)


    try:
        urllib.request.urlretrieve(url, "./cimg/cashedimage")
        imgd = Image.open("./cimg/cashedimage")
        img_dict[loadimagelist_count] = ImageTk.PhotoImage(imgd)
        #print(magic.from_file('./cimg/cashedimage', mime=True))
        filetype = imghdr.what("./cimg/cashedimage", h=None)
        if filetype != "gif":
            img_data_dict[loadimagelist_count] = Label(text, image=img_dict[loadimagelist_count])
            img_data_dict[loadimagelist_count].bind("<Button-1>",lambda boi: openinpreview(img))
            #img_data_dict[loadimagelist_count].pack(side=TOP)
            #return label

        else:
            img_data_dict[loadimagelist_count] = AnimatedGIF(text, "./cimg/cashedimage")
            img_data_dict[loadimagelist_count].start_animation()
            img_data_dict[loadimagelist_count].bind("<Button-1>", lambda boi: openinpreview(img))
            #img_data_dict[loadimagelist_count].pack(side=TOP)

    except FileNotFoundError:
        os.mkdir("cimg")
        urllib.request.urlretrieve(url, "./cimg/cashedimage")
        imgd = Image.open("./cimg/cashedimage")
        img_dict[loadimagelist_count] = ImageTk.PhotoImage(imgd)
        #print(magic.from_file('./cimg/cashedimage', mime=True))
        filetype = imghdr.what("./cimg/cashedimage", h=None)
        if filetype != "gif":
            img_data_dict[loadimagelist_count] = Label(text, image=img_dict[loadimagelist_count])
            img_data_dict[loadimagelist_count].bind("<Button-1>", lambda boi: openinpreview(img))
            #img_data_dict[loadimagelist_count].pack(side=TOP)
            #return label
        else:
            img_data_dict[loadimagelist_count] = AnimatedGIF(text, "./cimg/cashedimage")
            img_data_dict[loadimagelist_count].start_animation()
            img_data_dict[loadimagelist_count].bind("<Button-1>", lambda boi: openinpreview(img))
            #label.pack(side=TOP)


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
    try:
        out = requests.get(servboi)
        return out.text
    except:
        print("Server Connection Error")
        return "Error Connecting to Server"


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
    print(out)
    temp = requests.get(out)

def sendcmd(senddata):
    print("sendt")
    try:
        outline = senddata
    except TypeError:
        messagebox.showerror("Chat Noise Config Error", "You must have a username to send a message")
    servboi = "http://" + server + port + "?cmd="
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
    out = servboi + outline + "&id=" + addedout + "\n"
    temp = requests.get(out)


def setupdate():
    print("what does this do")
    global updategood
    updategood = not updategood


def sendread(a):
    print("read")
    try:
        bigboi = chatbox.get()
        if bigboi[0] == "@":
            sendcmd(bigboi)
        else:
            send(bigboi)
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
                                               "Developed By: InventorXtreme\n"
                                               "Client Version " + clientversion + ""
                                                                                   " using Tkinter GUI\n"
                                                                                   "Server Version: " + serverversion)


global imglistcount
imglistcount = 0

class HyperlinkManager:

    def __init__(self, text):

        self.text = text

        self.text.tag_config("hyper", foreground="blue", underline=1)

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                runweb(self.links[tag])
                return

#Top Bar
class TopBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets
        self.config(height=20,bg='gray10')
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)

global keeplist
keeplist = []
def imglistpopup():
    global imgpopup
    global img_data_dict
    global img_list
    global scrollFrame
    global  imglistcount
    global keeplist
    widget_list = all_children(scrollFrame)
    if imglistcount == 0:
        print("ree")
        keeplist = all_children(scrollFrame)

    for x in keeplist:
       widget_list = list(filter(lambda a: a != x, widget_list))
    print(widget_list)
    for item in widget_list:
        item.destroy()
    imglistcount += 1


global ref_count
ref_count = 0

global textlabellist
textlabellist = {}

global old_mid
global new_mid
old_mid = -1
new_mid = getid()
global isfirst
isfirst = True
def runweb(test):
    print(test)
    webbrowser.open(test,new=2)

global manupdate
manupdate = False

def manupdatecall():
    global manupdate
    manupdate = True

def refresh(h):
    global manupdate
    global new_mid
    global old_mid
    global textlabellist
    global ref_count
    global isfirst
    print("refeshed")
    while True:
        if isfirst != True:
            old_mid = new_mid
            new_mid = getid()


        if updategood != False and new_mid != old_mid:
            updateif = True
        if manupdate == True:
            manupdate = False
            updateif = True


        if updateif == True:
            updateif = False
            isfirst = False
            x = get_data()

            lines = get_lines()
            print(lines)
            #replace with a line list
            #interperet and insert
            if ref_count == ref_count:
                try:
                    imglistpopup()
                    imgextract()
                except tkinter.TclError:
                    pass
            linenum = 0
            linenumimage = len(lines)

            # text.delete('1.0',END)
            text.delete('1.0', END)
            text.insert(END, x)
            text.see(END)

            lineiddict = {}
            numused = 0
            linuse = 0
            res = list(img_data_dict.keys())[0]
            imgtextcount = int(res)
            imgtextcountend = int(res)+5
            print(img_data_dict)
            for i in lines:
                linenum = linenum+1
                if i[0] == "|" and i[1] == "l":
                    print("yea")
                    linematch = str(linenum+linuse)
                    linuse = linuse + 1
                    linegood = linematch + '.0'
                    linegood2 = linematch + '.1000'

                    lineiddict[linegood] = i[6:]
                    outstring = i[6:-1]
                    text.delete(linegood, linegood2)
                    outstring.replace('\n ','f').replace('\r','f')
                    text.insert(linegood,outstring,hyperlink.add(i[6:]))
                    text.see(END)
                    print(linegood)
                    linenum = linenum-1
            lines = get_lines()

            for i in reversed(lines):
                if i[0] == "i" and i[1] == "m" and i[2]=="g" and i[3] == "|" and imgtextcount != imgtextcountend:
                    print("yea")
                    linematch = str(linenumimage)
                    linegood = linematch + '.0'
                    linegood2 = linematch + '.1000'
                    #text.delete(linegood, linegood2)
                    #text.insert(linegood, i[6:], hyperlink.add(lambda: runweb(i[6:])))
                    text.see(END)
                    print(linegood)
                    #print(img_data_dict)
                    print(imgtextcount)
                    print(i)
                    #try:
                        #text.image_create(linegood, image=img_data_dict[imgtextcount])
                    #except:

                    text.window_create(linegood, window=img_data_dict[imgtextcount])
                    imgtextcount += 1
                linenumimage -= 1

            ref_count += 1
            text.tag_configure("red", foreground="Red")
            text.tag_configure("blue",foreground="#00c0FF")
            text.tag_configure("green",foreground="#00ff00")
            text.highlight_pattern("/.*:", "blue", regexp=True,start="end-25l")
            text.highlight_pattern("=.*:", "green",regexp=True,start="end-25l")
            text.highlight_pattern("-.*:", "red", regexp=True,start="end-25l")
            text.highlight_pattern(r"\(DEV\)", "blue", regexp=True,start="end-10l")
            time.sleep(3)
        else:
            ref_count = 5
            time.sleep(3)

def img_post(filename):
    out = "img|" + filename
    sendnbs(out)

root = Tk()


mainbar = TopBar(root)
mainbar.pack(fill='x',side=TOP)

m = Frame(root)
m.pack(fill=BOTH, expand=1)
root.configure(background='grey10')
Title = "Electric Boogaloo Chat Noise Client " + clientversion
root.title(Title)
root.bind('<Return>', sendread)

chatboxframe = Frame(m, bg="grey10")
chatboxframe.pack(side="left",expand=True,fill=BOTH)
#m.add(chatboxframe)
text = CustomText(chatboxframe, bg="grey10", fg="white",font = ('Biome', 13))
text.pack(expand=True,fill=BOTH)
hyperlink = HyperlinkManager(text)
chatbox = Entry(chatboxframe, width=20, bg="grey10", fg="white",font = ('Biome', 13))
chatbox.pack(side=LEFT,expand=True,fill=BOTH)
chatbox.config(insertbackground="#FFFFFF")

sendb = Button(chatboxframe, command=sendreadb, text="send", bg="grey10", fg="red3",height=1,width=7)
sendb.pack(side=RIGHT)


#menubar = Menu(root)

#Plugs = Menu(root)

settingsmenu = Menu(root, background='gray10', foreground='white',
               activebackground='#004c99', activeforeground='white',
                    tearoff=0)


settingsmenu.add_command(label="Change Username", command=changename)
settingsmenu.add_command(label="Change Server", command=changeserver)
settingsmenu.add_command(label="Change Port", command=changeport)

codemenu = Menu(root, background='gray10', foreground='white',
               activebackground='#004c99', activeforeground='white',
                tearoff=0)



def imglistpopup_caller():
    global imgpopup
    imgpopup = tkinter.Toplevel(root)
    imglistpopup()
def send_link():
    base64_img = simpledialog.askstring("Chat Noise -> Link", "Input link to send")
    out = "|link|" + base64_img
    sendnbs(out)
codemenu.add_command(label="Upload", command=uploadimage)
codemenu.add_command(label="Post Image",command=embedup)
codemenu.add_command(label="Open in Browser", command=loadimagebrowser)
#codemenu.add_command(label="Post Image(Legacy)", command=img_sause)
codemenu.add_command(label="Send Link", command=send_link)

FileMenu = Menu(root, background='gray10', foreground='white',
               activebackground='#004c99', activeforeground='white',
                tearoff=0)

# FileMenu.add_command(label="Settings",command=settings)

FileMenu.add_command(label="Manual Refresh", command=manupdatecall)
FileMenu.add_command(label="Send Clipboard", command=send_clip)
FileMenu.add_command(label="About", command=about)

#legacy menubar code
# menubar.add_cascade(label="File", menu=FileMenu)
# menubar.add_cascade(label="Encode/Decode Images", menu=codemenu)
# menubar.add_cascade(label="Settings", menu=settingsmenu)
#(menu=menubar)

#Top Menubar code
def do_file_popup(event):
    # display the popup menu
    try:
        FileMenu.tk_popup(event.x_root, event.y_root+15, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        FileMenu.grab_release()

def do_code_popup(event):
    # display the popup menu
    try:
        codemenu.tk_popup(event.x_root, event.y_root+15, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        codemenu.grab_release()

def do_settings_popup(event):
    # display the popup menu
    try:
        settingsmenu.tk_popup(event.x_root, event.y_root+15, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        settingsmenu.grab_release()

#File Dropdown
FileDropdown = Label(mainbar,text="File",bg="gray10",fg='white')
FileDropdown.pack(side="left")
FileDropdown.bind("<Button-1>", do_file_popup)

spacer1 = Label(mainbar,text="  ",bg="gray10")
spacer1.pack(side='left')

CodemenuDropdown = Label(mainbar,text='Special',bg='gray10',fg='white')
CodemenuDropdown.pack(side='left')
CodemenuDropdown.bind("<Button-1>", do_code_popup)

spacer2 = Label(mainbar,text="  ",bg="gray10")
spacer2.pack(side='left')

settingsmenudropdown = Label(mainbar,text='Settings',bg='gray10',fg='white')
settingsmenudropdown.pack(side='left')
settingsmenudropdown.bind("<Button-1>", do_settings_popup)
try:
    urllib.request.urlretrieve("https://raw.githubusercontent.com/InventorXtreme/ChatNoise/master/version", "version")
    versionfile = open("version","r+")
    content = versionfile.read()
except:
    print("versionerror")
    content = clientversion


is_adminp = ctypes.windll.shell32.IsUserAnAdmin()
if is_adminp == 1:
    is_admin = True
else:
    is_admin = False


if content == clientversion:
    print("No Updates")
else:
    versionmenu = messagebox.askquestion(title="Electic Boogaloo Update", message="Update found!\n"
                                                                               "Your Version :" + clientversion + "\n"
                                                                               "New Version: "+ content + "\n"
                                                                                                          "Update to new version?")
    if versionmenu == "yes":
        download_folder = os.path.expanduser("~") + "/Downloads/"
        snip = content[2:]
        url = "https://github.com/InventorXtreme/ChatNoise/releases/download/"+snip + "/setup.exe"
        print(url)
        #messagebox.showinfo("Downloading Update...","Downloading Update...")
        if is_admin == False:
            messagebox.showerror("Admin Rights", "Admin rights are required to update this program,\n"
                                                 "Please relaunch the program by right clicking on the desktop icon\n"
                                                 "and selecting Run as Administrator and approving the request.")
            root.quit()

        urllib.request.urlretrieve(url, r"C:\temp\setup.exe")
        #messagebox.showinfo("Update", "Please press OK to install the update")
        #messagebox.showwarning("Installing update",
        #                       "The program will close after the installation,to finish the install, please reopen it")
        os.startfile(r"C:\temp\setup.exe")
        exit()


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

def get_lines():
    print("display Lines")
    iservboi = "http://" + server + port + "?get"
    try:
        down = requests.get(iservboi)
    except requests.exceptions.ConnectionError:
        return "Error Connecting to server"
    x = down.text
    with open("chatlogclient.txt", "w+") as file:
        file.write(x)
    with open("chatlogclient.txt", 'r') as fin:
        return fin.readlines()

global img_list
img_list = {}
scrollFrame = ScrollFrame(root)
scrollFrame.viewPort.config(bg="grey10")
#scrollFrame.pack(side="left",expand=True,fill=BOTH)
#m.add(scrollFrame)
def imgextract():
    #imglistpopup()
    global img_list
    global img_names
    global imgpopup
    global scrollFrame
    global img_data_dict
    img_list.clear()
    cnt = 1
    cntimg = 0
    iservboi = "http://" + server + port + "?get"
    #scrollFrame = ScrollFrame(root)  # add a new scrollable frame.
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
        img_data_dict = {}
        img_dict = {}

        while True:
            goto = False
            try:
                line = linelist[cnt]
            except IndexError:
                break

            command = line.split("|")
            if command[0] == "img" and cntimg < 5:
                #come back
                img_list[command[1]] = loadimagelist(command[1])
                img_names.append(command[1])
                cntimg += 1

            cnt += 1
    #scrollFrame.pack(side="left")



GuiLoop = threading.Thread(target=refresh, args=(1,), daemon=True)
GuiLoop.start()

root.mainloop()