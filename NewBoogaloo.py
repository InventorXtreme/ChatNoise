import tkinter as tk
import EBWidgetLib as EBLib
import requests
import threading
import time
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
from elevate import elevate
from tkinter import filedialog
import os
from tkinter import simpledialog
import shutil
import gc
#from cefpython3 import cefpython as cef
try:
    from ctypes import windll
    win = True
except:
    win = False
import ctypes
import urllib
import pickle
import sys
import dill
#from browser import *
global root
global topbar
global main
#elevate()


# NOTE TO FUTURE SELF
# use --add-data VLC;.\\VLC in pyinstaller to get vlc workin

class TextInputBlock(tk.Frame):
    def __init__(self,parent,server,port,username,font,*args,**kwargs):
        self.font= font
        self.server = server
        self.port = port
        self.username = username
        self.parent = parent
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.chatbox = tk.Entry(self,width=20,font=self.font,bg="gray10",fg="white",insertbackground="white")
        self.chatbox.bind('<Control-BackSpace>', self.entry_ctrl_bs)
        self.chatbox.pack(fill=tk.X,side=tk.LEFT,expand=True)
        self.sendbutton = tk.Button(self,height=1,width=6,text="send",command=self.send,bg="gray10",fg="white")
        self.sendbutton.pack(side=tk.RIGHT)
        self.chan = ""
    def entry_ctrl_bs(self,event):
        ent = event.widget
        end_idx = ent.index(tk.INSERT)
        start_idx = ent.get().rfind(" ", None, end_idx)
        ent.selection_range(start_idx, end_idx)

    def send(self,*args):
        self.text = self.chatbox.get()
        if self.text != "":
            if self.text != len(self.text) * self.text[0] and self.text[0] != " ":
                self.url = self.server + ":" + self.port + "?send=" + self.username + ": " + self.text + "&id=" + self.getid()
                if self.chan != "":
                    self.url = self.url + "&channel="+self.chan
                outboundrequest = requests.get(url=self.url)
                print(self.url)
                print(outboundrequest)
                self.chatbox.delete(0,tk.END)
    def sendimage(self,*args):
        self.serverurl =  self.server + ":" + self.port + "/upimage/"
        self.filename = filedialog.askopenfilename(
            filetypes=(("Images", "*.jpg"), ("Images", "*.png"), ("Images", "*.jpeg"), ("Images", "*.gif")))
        try:
            with open(self.filename, 'rb') as filedata:
                self.imgrequest = requests.post(self.serverurl, files={'file': filedata})
                self.outname = os.path.basename(filedata.name)
                self.imageurl = self.server + ":" + self.port + "?send=" + "img|" + self.outname + "&id=" + self.getid()
                if self.chan != "":
                    self.imageurl = self.imageurl + "&channel=" + self.chan
                self.outimgrequest = requests.get(url=self.imageurl)
        except:
            print("EmbedUp error")
            pass
    def sendlink(self,*args):
        self.linkname = simpledialog.askstring("Chat Noise -> Link", "Input link to send")
        self.url = self.server + ":" + self.port + "?send=" + "|link|" + self.linkname + "&id=" + self.getid()
        if self.chan != "":
            self.url = self.url + "&channel="+self.chan
        self.lrequest = requests.get(url=self.url)

    def sendyte(self,*args):
        self.linkname = simpledialog.askstring("Chat Noise -> Link", "Input YoutubeEmbed to send")
        self.url = self.server + ":" + self.port + "?send=" + "|yte|" + self.linkname + "&id=" + self.getid()
        if self.chan != "":
            self.url = self.url + "&channel="+self.chan
        self.lrequest = requests.get(url=self.url)

    def getid(self):
        self.res = EBLib.getid(self.server,self.port)
        self.out = str(int(self.res) + 1)
        return self.out
    def setchan(self,channel):
        self.chan = channel


class ChatReadOut(tk.Frame):
    def __init__(self,parent,server,port,font,imageback,*args,**kwargs):
        self.server = server
        self.port = port
        self.font = font
        self.parent = parent
        self.imageback = imageback
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.textbox = EBLib.CustomText(self,font=self.font)
        self.textbox.config(state=tk.DISABLED)
        self.textbox.config(bg="gray10",fg="white")
        self.hypeman = EBLib.HyperlinkManager(self.textbox)
        self.textbox.pack(fill=tk.BOTH,expand=True)

        self.chan = ""
        self.threadlist = []
        self.imgrenderdict = {}
        self.imglist = {}
        self.imgdata = {}
        self.ytelist = {}
        self.ytedata = {}

        self.linklist = {}

        self.old = "ree"
        self.new = "r"
        self.bind("<Configure>", self.configure)
    def trigger(self):
        self.new = "-20"
        self.old = "-20"
        print("[USER] MANNUAL REFRESH TRIGGERED")
    def configure(self,event):
        self.textbox.see(tk.END)
    def runable(self):
        while True:
            self.old = self.new
            self.new = EBLib.getid(self.server,self.port)
            #print(self.old,self.new)
            if self.new != self.old:
                self.refresh()
                print("[RUNABLE THREAD] REFRESHED")
                time.sleep(2)
    def refresh(self):
        print("[REFRESH] STARTING REFRESH")
        self.imglist = {}
        self.ytelist = {}
        self.linklist = {}

        self.richthread = threading.Thread(target=self.richimg)
        self.highlightthread = threading.Thread(target=self.highlight)
        self.ytethread = threading.Thread(target=self.richytembed)
        self.textbox.config(state=tk.NORMAL)
        self.textbox.see(tk.END)
        self.url = self.server + ":" + self.port + "?get"
        if self.chan != "":
            self.url = self.url + "&channel="+self.chan
        self.incommingdata = requests.get(self.url)
        self.downloadedtext = self.incommingdata.text
        self.lines = self.downloadedtext.split("\n")
        #print(self.lines)
        self.lines.reverse()

        self.linenum = len(self.lines)
        #print(self.linenum)
        self.imgcount = 0

        for self.currentline in self.lines:
            self.linenum -= 1
            #print(self.currentline)
            #print(self.linenum)
            try:
                if self.currentline[0] == "i" and self.currentline[1] =="m" and self.currentline[2] =="g" and self.currentline[3] == "|":
                    if self.imgcount != self.imageback:
                        self.imglist[self.linenum] = self.currentline[4:]
                        self.imgcount += 1
                if self.currentline[0] == "|" and self.currentline[1] == "l":
                    self.linklist[self.linenum] = self.currentline[6:]
                if self.currentline[0] == "|" and self.currentline[1] == "y":
                    if self.imgcount != self.imageback:
                        self.ytelist[self.linenum] = self.currentline[5:]
                        self.imgcount += 1

            except:
                pass

        self.textbox.delete('1.0', tk.END)
        self.textbox.insert('1.0', self.downloadedtext)
        #print(self.linklist,self.imglist,self.ytelist)
        self.richthread.start()
        self.highlightthread.start()
        self.ytethread.start()
        self.richlink()
        # Old rich text code was here before multithreaded

        self.textbox.config(state=tk.DISABLED)
        #self.richytembed()
        self.richthread.join()
        self.highlightthread.join()
        self.ytethread.join()
        print("[REFESH] OK")

    def setchan(self,channel):
        self.chan = channel

    def highlight(self):
        self.textbox.tag_configure("blue", foreground="#00c0FF")
        self.textbox.tag_configure("red", foreground="#ff0000")
        self.textbox.tag_configure("green", foreground="#00ff00")
        self.textbox.highlight_pattern("/.*:", "blue", regexp=True, start="end-25l")
        self.textbox.highlight_pattern("=.*:", "green", regexp=True, start="end-25l")
        self.textbox.highlight_pattern("-.*:", "red", regexp=True, start="end-25l")
        self.textbox.see(tk.END)

    def richytembed(self):
        print("[RICH EMBEDS] Starting Rich YTE")
        for self.tempyte in self.ytedata:
            self.ytedata[self.tempyte].end()
            self.ytedata[self.tempyte].destroy()

        self.ytedata.clear()
        gc.collect()
        #print(self.ytedata)

        for self.yterender in self.ytelist:
            print("[RYTE] Rendered one embed")
            self.ytedata[self.yterender] = EBLib.YoutubeEmbed(self.textbox,self.ytelist[self.yterender],self.yterender,width=200,height=100)
            #self.ytedata[self.yterender].pack()
            self.ytestring = str(self.yterender) + ".0"
            self.textbox.window_create(self.ytestring,window=self.ytedata[self.yterender])
            self.textbox.see(tk.END)

    def richimg(self):
        self.loadednum = 0
        self.imagenum = 0

        for self.temp in self.imgdata:
            self.imgdata[self.temp].destroy()
        self.imgdata.clear()
        gc.collect()
        #topbar.statuschange("")

        for self.imgrender in self.imglist:
            try:
                topbar.pro.pack(side=tk.RIGHT)
            except NameError:
                pass
            self.imagenum += 1
            self.icment = 100 / self.imageback
            self.icment = self.icment / 2
            #TODO Make each image load individualy from eachother
            self.string = self.imglist[self.imgrender]
            self.ctrtrue = self.string.find(" ")
            if self.ctrtrue != -1:
                self.imglist[self.imgrender] = "404error.png"
            self.prepstring = str(self.imgrender) + ".0"
            #topbar.pro.step(self.icment)
            #topbar.statuschange("Loading Image " + str(self.imagenum) +  "/" +str(self.imageback) + "   ")
            thread = threading.Thread(target=self.image_loader,args=[self.imgrender,self.imagenum])
            self.threadlist.append(thread)
            thread.start()
            # self.imgdata[self.imgrender] = EBLib.ImageChatFrame(self.textbox,self.imglist[self.imgrender],self.server,self.port,self.imgrender)
            # self.textbox.window_create(self.prepstring, window=self.imgdata[self.imgrender])
            # print(self.imgrender,self.imglist[self.imgrender])
            #topbar.pro.step(self.icment)
        for self.thread in self.threadlist:
            self.thread.join()
        self.textbox.see(tk.END)



            # if self.imagenum == self.imageback:
            #     topbar.statuschange("Ready   ")
            #     topbar.pro.pack_forget()
        try:
            topbar.statuschange("Ready   ")
            topbar.pro['value'] = 0
            topbar.pro.pack_forget()
        except NameError:
            pass
    def richlink(self):
        for self.linkrender in self.linklist:
            self.outstring = self.linklist[self.linkrender]
            self.linegood = str(self.linkrender+1) + ".0"
            self.lineclear = str(self.linkrender+1) + ".999999999"
            self.textbox.delete(self.linegood,self.lineclear)
            print("rendering link at" + self.linegood + "with value of " + self.outstring)
            self.textbox.insert(self.linegood, self.outstring, self.hypeman.add(self.outstring))
            self.textbox.see(tk.END)
    def image_loader(self,render,id):

        self.imgrenderdict[id] = render
        self.int_imgrender = render
        self.int_prepstring = str(self.imgrenderdict[id]) + ".0"
        try:
            topbar.pro.step(self.icment)
        except NameError:
            pass

        self.imgdata[self.imgrenderdict[id] ] = EBLib.ImageChatFrame(self.textbox, self.imglist[self.imgrenderdict[id] ], self.server,
                                                            self.port, self.imgrenderdict[id] )
        self.textbox.window_create(str(self.imgrenderdict[id])+".0", window=self.imgdata[self.imgrenderdict[id] ])
        print("rendering image at" + self.imgrenderdict[id] + "with data of " + self.imglist[self.imgrenderdict[id] ])

        self.imgdata[self.imgrenderdict[id] ].widget.bind("<MouseWheel>", scroll_parent)
        self.imgdata[self.imgrenderdict[id] ].bind("<MouseWheel>", scroll_parent)
        self.loadednum += 1
        try:
            topbar.pro.step(self.icment)
            topbar.statuschange("Loading Image " + str(self.loadednum) + "/" + str(self.imageback) + "   ")
        except NameError:
            pass

        self.textbox.see(tk.END)




class EBClient(tk.Frame):
    def __init__(self,parent,server,port,username,imgback,*args,**kwargs):
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.server = server
        self.username = username
        self.port = port
        self.imgback = imgback
        self.chatbox = ChatReadOut(self,self.server,self.port,('OCR A', 13),self.imgback)
        self.ebox = TextInputBlock(self,self.server,self.port,self.username,font = ('OCR A', 13))
        self.chatbox.pack(fill=tk.BOTH, expand=True)
        self.ebox.pack(fill=tk.X, side=tk.TOP)
    def changechan(self,channelchange):
        self.chatbox.setchan(channelchange)
        self.ebox.setchan(channelchange)
        self.chatbox.trigger()




class MenuAdd(tk.Frame):
    global main
    global audio
    global pane
    def __init__(self,parent,server,port,clientversion,*args,**kwargs):
        #s = ttk.Style()
        #s.theme_use("")
        self.clientversion = clientversion
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.server = server
        self.port = port
        self.mainbar = EBLib.TopBar(self.parent)
        self.statbar = EBLib.TopBar(self.parent)
        #self.bigboiroot = bigboiroot
        # MENUBAR CODE //todo: Make OOP
        self.FileMenu = tk.Menu(parent, background='gray10', foreground='white',
                                activebackground='#004c99', activeforeground='white',
                                tearoff=0)
        self.FileDrop = tk.Label(self.mainbar, text="File", bg="gray10", fg="white")

        self.FileDrop.bind("<Button-1>",self.do_file_popup)
        self.spacer = tk.Label(self.statbar, text="    ", bg="gray10")
        self.spacer2 = tk.Label(self.mainbar,text=" ",bg="gray10")

        self.SendMenu = tk.Menu(parent, background='gray10', foreground='white',
                                activebackground='#004c99', activeforeground='white',
                                tearoff=0)
        self.SendDrop = tk.Label(self.mainbar,text="Send  ",bg="gray10",fg="white")
        self.SendDrop.bind("<Button-1>",self.do_send_popup)
        self.SetMenu = tk.Menu(parent, background='gray10', foreground='white',
                                activebackground='#004c99', activeforeground='white',
                                tearoff=0)

        #self.AudioDrop = tk.Label(self.mainbar,text="Audio",bg="gray10",fg="white")
        #self.AudioDrop.bind("<Button-1>",self.do_audio_popup)
        #self.AudioMenu = tk.Menu(parent, background='gray10', foreground='white',
        #                        activebackground='#004c99', activeforeground='white',
        #                        tearoff=0)
        self.SetDrop = tk.Label(self.mainbar,text="Settings",bg="gray10",fg="white")
        #TODO: MAKE SETTINGS
        self.SetDrop.bind("<Button-1>",self.do_set_popup)
        self.spacer = tk.Label(self.statbar,text="    ",bg="gray10")
        self.pro = ttk.Progressbar(self.statbar,length=200)
        self.status = tk.Label(self.statbar, text="Ready   ",bg="gray10",fg="white")
        self.status.pack(side=tk.LEFT)
        self.mainbar.pack(fill='x', side=tk.TOP)
        self.statbar.pack(fill='x', side=tk.BOTTOM)
        self.FileDrop.pack(side=tk.LEFT)
        self.spacer.pack(side=tk.RIGHT)
        self.spacer2.pack(side=tk.LEFT)
        self.SendDrop.pack(side=tk.LEFT)
        #self.AudioDrop.pack(side=tk.LEFT)
        self.SetDrop.pack(side=tk.LEFT)
        self.spacer.pack(side=tk.RIGHT)
        self.pro.pack(side=tk.RIGHT)



    def statuschange(self,text):
        self.text = text
        self.status.config(text=self.text)
    def linker(self,ebcontroller):
        self.ebcontroller=ebcontroller
        self.FileMenu.add_command(label="Refresh", command=self.ebcontroller.chatbox.trigger)
        #self.FileMenu.add_command(label="DooDooCord",command=self.doodoocord)
        self.FileMenu.add_command(label="About",command=self.about)

        self.SendMenu.add_command(label="Send Image", command = self.ebcontroller.ebox.sendimage)
        self.SendMenu.add_command(label="Send Link",command=self.ebcontroller.ebox.sendlink)
        self.SendMenu.add_command(label="Add Channel",command=self.addchan)
        self.SendMenu.add_command(label="Send YTE",command=self.ebcontroller.ebox.sendyte)

        self.FileMenu.add_command(label="Back to Main Channel",command=lambda: main.changechan(""))

        self.SetMenu.add_command(label="Change Username",command=changename)
        self.SetMenu.add_command(label="Change Port", command=changeport)
        self.SetMenu.add_command(label="Change Server", command=changeserver)
        #self.SetMenu.add_command(label="Change Audio Server",command=changeaudioserver)
        #self.SetMenu.add_command(label="Change Audio Port",comman=changeaudioport)
        self.SetMenu.add_command(label="Change ImageNumber",command=changeimgload)

        #self.AudioMenu.add_command(label="Connect",command=audio.connect)
        #self.AudioMenu.add_command(label="Disconnect",command=audio.disconnect)
    def do_file_popup(self,event):
        # display the popup menu
        try:
            self.FileMenu.tk_popup(event.x_root, event.y_root + 15, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.FileMenu.grab_release()

    def do_send_popup(self,event):
        # display the popup menu
        try:
            self.SendMenu.tk_popup(event.x_root, event.y_root + 15, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.SendMenu.grab_release()

    def do_set_popup(self,event):
        # display popup
        try:
            self.SetMenu.tk_popup(event.x_root, event.y_root + 15,0)
        finally:
            self.SetMenu.grab_release()

    #def do_audio_popup(self,event):
    #    try:
    #        self.AudioMenu.tk_popup(event.x_root, event.y_root + 15,0)
    #    finally:
    #        self.AudioMenu.grab_release()

    def about(self):
        print("[USER] ABOUT BOX OPENED")
        try:
            self.aurl = self.server + ":" + self.port + "/ver"
            self.temp = requests.get(self.aurl)
            self.serverversion = self.temp.text
            #print(self.serverversion)
        except:
            self.serverversion = "Error connecting to server"

        messagebox.showinfo(title="About", message="ChatNoise -> A chat client/protocol for the people\n"
                                                   "Developed By: InventorXtreme\n"
                                                   "Client Version " + self.clientversion + ""
                                                                                       " using Tkinter GUI\n"
                                                                                       "Server Version: " + self.serverversion)
    def addchan(self):
        self.newchan = simpledialog.askstring("Make New Channel", "Enter The name of the channel")
        self.lazy = self.server+":" + self.port + "/addchan/" + "?newchan=" + self.newchan
        self.bigboi = requests.get(self.lazy)




def checkupdates(versionu):
    #print(versionu)
    try:    
        is_adminp = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        pass
        is_adminp = 1
    if is_adminp == 1:
        is_admin = True
    else:
        is_admin = False
    verrequest = requests.get(url="https://raw.githubusercontent.com/InventorXtreme/ChatNoise/master/version")
    if versionu == verrequest.text:
        pass
    else:
        versionmenu = messagebox.askquestion(title="Electic Boogaloo Update", message="Update found!\n"
                                                                                "Your Version :" + versionu + "\n"
                                                                                "New Version: " + verrequest.text + "\n"
                                                                                "Update to new version?")
        if versionmenu == "yes":
            download_folder = os.path.expanduser("~") + "/Downloads/"
            snip = verrequest.text[2:]
            url = "https://github.com/InventorXtreme/ChatNoise/releases/download/" + snip + "/setup.exe"
            #print(url)
            # messagebox.showinfo("Downloading Update...","Downloading Update...")
            if is_admin == False:
                root.destroy()
                elevate()
            else:
                #urllib.request.urlretrieve(url, r"C:\temp\setup.exe")
                setupfile = requests.get(url)
                with open(r'C:\temp\setup.exe') as helpme:
                    helpme.write(setupfile.content)
                exit()


def changename():
    global username,server,port,audioserver,audioport
    config = pickle.load(open("config.p", "rb"))
    namesetup = simpledialog.askstring("Setup", "Please Enter Your Username")
    if len(namesetup) < 16:
        config["username"] = namesetup
        pickle.dump(config, open("config.p", "wb+"))
        config = pickle.load(open("config.p", "rb"))
        username = config["username"]
        server = config["server"]
        port = config["port"]
        messagebox.showinfo("Info","Please Restart ChatNoise to apply changes")
    else:
        messagebox.showerror("Setup", "Uesrnames must be 15 characters or less")


def changeport():
    global username,server,port,audioserver,audioport
    config = pickle.load(open("config.p", "rb"))
    portsetup = simpledialog.askstring("Setup", "Please Enter Your Port")
    config["port"] = portsetup
    pickle.dump(config, open("config.p", "wb+"))
    config = pickle.load(open("config.p", "rb"))
    username = config["username"]
    server = config["server"]
    port = config["port"]
    messagebox.showinfo("Info","Please Restart ChatNoise to apply changes")


def changeserver():
    global username,server,port,audioserver,audioport
    config = pickle.load(open("config.p", "rb"))
    serversetup = simpledialog.askstring("Setup", "Please Enter Your Server Including The http(s)://")
    config["server"] = serversetup
    pickle.dump(config, open("config.p", "wb+"))
    config = pickle.load(open("config.p", "rb"))
    username = config["username"]
    server = config["server"]
    port = config["port"]
    messagebox.showinfo("Info","Please Restart ChatNoise to apply changes")

def changeimgload():
    global username,server,port,audioserver,audioport
    config = pickle.load(open("config.p", "rb"))
    imgnumsetup = int(simpledialog.askstring("Setup", "Please Enter the number of images to load"))
    config["imgnum"] = imgnumsetup
    pickle.dump(config, open("config.p", "wb+"))
    config = pickle.load(open("config.p", "rb"))
    username = config["username"]
    server = config["server"]
    port = config["port"]
    imgnum = config["imgnum"]
    messagebox.showinfo("Info","Please Restart ChatNoise to apply changes")

def changeaudioserver():
    global username,server,port,audioserver,audioport
    config = pickle.load(open("config.p", "rb"))
    aussetup = simpledialog.askstring("Setup", "Please Enter the server for audio")
    config["audioserver"] = aussetup
    pickle.dump(config, open("config.p", "wb+"))
    config = pickle.load(open("config.p", "rb"))
    username = config["username"]
    server = config["server"]
    port = config["port"]
    imgnum = config["imgnum"]
    messagebox.showinfo("Info","Please Restart ChatNoise to apply changes")

def changeaudioport():
    global username,server,port,audioserver,audioport
    config = pickle.load(open("config.p", "rb"))
    aussetupp = simpledialog.askstring("Setup", "Please Enter the port for audio")
    config["audioport"] = aussetupp
    pickle.dump(config, open("config.p", "wb+"))
    config = pickle.load(open("config.p", "rb"))
    username = config["username"]
    server = config["server"]
    port = config["port"]
    imgnum = config["imgnum"]
    messagebox.showinfo("Info","Please Restart ChatNoise to apply changes")

def scroll_parent(event):
    parent = root.nametowidget(event.widget.winfo_parent())
    parent.event_generate("<MouseWheel>", delta=event.delta, when="now")

def on_closing():
    folder = './cimg'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print("[KILLIT] CLEARED IMAGE CACHE")
    for item in main.chatbox.ytedata:
        main.chatbox.ytedata[item].end()
        main.chatbox.ytedata[item].destroy()
    root.destroy()
def mainfunc():
    global clientversion
    global root
    global topbar
    global main
    global audio
    global audioman
    global pane
    try:
        if sys.argv[1] == "-u":
            elevate()

    except:
        #elevate()
        pass
    #server = "https://inventorxtreme19.pythonanywhere.com"
    #username = "/Alex"
    #port = "443"
    try:
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    root = tk.Tk()
    switches = {
        "enable-media-stream": "",
        "use-fake-ui-for-media-stream": "",}
    no = {}
    #cef.Initialize(no,switches)
    root.title("Electric Boogaloo Chat Noise Client" + clientversion)

    try:
        config = pickle.load(open("config.p", "rb"))
        audioserver = config["audioserver"]
        print("[STARTIT] LOADED AUDIOSERVER VALUE")
        audioport = config["audioport"]
        print("[STARTIT] LOADED AUDIOPORT VALUE")

        username = config["username"]
        print("[STARTIT] LOADED USERNAME VALUE")

        server = config["server"]
        print("[STARTIT] LOADED SERVER VALUE")

        port = config["port"]
        print("[STARTIT] LOADED PORT VALUE")

        imgnum = int(config["imgnum"])
        print("[STARTIT] LOADED IMGNUM VALUE")

        print("[STARTIT] CONFIG LOADED")
        try:
            audio = EBLib.Client(audioserver,audioport,root)
        except:
            audio = EBLib.Client(audioserver,722,root)
    except:
        print("CONFIG ERROR: SETTING UP")
        namesetup = simpledialog.askstring("Setup","Please enter your username")
        serversetup = simpledialog.askstring("Setup","Please enter your server including the http:// or https://")
        portsetup = simpledialog.askstring("Setup","Please enter your port")
        imgnumsetup = int(simpledialog.askstring("Setup", "Please enter the number of images to load"))
        #audioserversetup = simpledialog.askstring("Setup","Please enter the server to use for audio")
        #audioport = simpledialog.askstring('Setup', "Please enter the port to use for audio")
        audioserversetup = ""
        audioport = "0"
        config = {}
        if isinstance(imgnumsetup, (int, float, complex)) and not isinstance(imgnumsetup, bool):
            config["server"] = serversetup
            config["port"] = portsetup
            config["username"] = namesetup
            config["imgnum"] = imgnumsetup
            config["audioserver"] = audioserversetup
            config["audioport"] = audioport
            pickle.dump(config, open("config.p", "wb+"))
            config = pickle.load(open("config.p", "rb"))
            username = config["username"]
            server = config["server"]
            imgnum = config["imgnum"]
            port = config["port"]
            audioserver = config["audioserver"]
            audioport = config["audioport"]
            print("config loaded")
            audio = EBLib.Client(audioserver, audioport,root)

        else:
            root.destroy()


    print(username)




    topbar = MenuAdd(root, server, port,clientversion)


    pane = tk.PanedWindow()


    pane.pack(expand=True,fill=tk.BOTH)

    # WHAT EVER YOU DO, DO NOT MOVE MAIN ABOVE THE PANE LINE

    main = EBClient(root, server, port, username, imgnum)

    try:
        chanurl = server+ ":" +port + "/chanlist/"
        print("[STARTIT] LOADING CHANLIST FROM " +chanurl)


        chanlist = EBLib.ChannelListBox(root, main, bg="gray10")
        chanlist.pack_propagate()
        pane.add(chanlist, stretch="always")
        pane.add(main)
        #urllib.request.urlretrieve(chanurl, "channellist.txt")
        r = requests.get(chanurl)


        # chanlist.pack(fill=tk.Y,side=tk.LEFT)
        #audioman = EBLib.AudioMan(chanlist, audio, bg="gray10")
        #audioman.pack()


        #pane.add(audioman, stretch="always")
        root.update_idletasks()
        root.update()
        with open("channellist.txt", 'wb') as hhhh:
            hhhh.write(r.content)
        chanlist.loadlist()
        ChanListGood = True
    except:
        print("The channel list could not be loaded, this could indicate a problem with the server/port")
        pane.add(main)

        ChanListGood = False



    topbar.linker(main)
    root.update_idletasks()
    #checkupdates(clientversion)
    rethread = threading.Thread(target=main.chatbox.runable,daemon=True)
    rethread.start()
    #main.pack(expand=1)

    #pane.add(subpane)

    try:
        pane.sash_place(0,150,0)
    except:
        pass
    root.bind('<Return>', main.ebox.send)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    main.chatbox.focus_set()



    root.mainloop()
    audio.disconnect()


if __name__ == "__main__":
    clientversion = "- 0.11.0"
    x=0


    try:
        file2 = open("hj.txt", "rb")
        bigboi = dill.load(file2)
        file2.close()
        x = 20
        bigboi()
    except:
        if x != 20:
            mainfunc()
