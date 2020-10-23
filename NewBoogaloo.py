import tkinter as tk
import EBWidgetLib as EBLib
import requests
from ctypes import windll
import threading
import time
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
from elevate import elevate
#elevate()
class TextInputBlock(tk.Frame):
    def __init__(self,parent,server,port,username,font,*args,**kwargs):
        self.font= font
        self.server = server
        self.port = port
        self.username = username
        self.parent = parent
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.chatbox = tk.Entry(self,width=20,font=self.font,bg="gray10",fg="white",insertbackground="white")
        self.chatbox.pack(expand=True,fill=tk.BOTH,side=tk.LEFT)
        self.sendbutton = tk.Button(self,height=1,width=6,text="send",command=self.send,bg="gray10",fg="white")
        self.sendbutton.pack(side=tk.RIGHT)
    def send(self,*args):
        self.text = self.chatbox.get()
        self.url = self.server + ":" + self.port + "?send=" + self.username + ": " + self.text + "&id=" + self.getid()
        outboundrequest = requests.get(url=self.url)
        print(self.url)
        print(outboundrequest)
        self.chatbox.delete(0,tk.END)
    def getid(self):
        self.res = EBLib.getid(self.server,self.port)
        self.out = str(int(self.res) + 1)
        return self.out


class ChatReadOut(tk.Frame):
    def __init__(self,parent,server,port,font,imageback,*args,**kwargs):
        self.server = server
        self.port = port
        self.font = font
        self.parent = parent
        self.imageback = imageback
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.textbox = EBLib.CustomText(font=self.font)
        self.textbox.config(state=tk.DISABLED)
        self.textbox.config(bg="gray10",fg="white")
        self.hypeman = EBLib.HyperlinkManager(self.textbox)
        self.textbox.pack(fill=tk.BOTH,expand=True)

        self.old = "ree"
        self.new = "r"
        self.bind("<Configure>", self.configure)
    def trigger(self):
        self.new = "-20"
        self.old = "-20"
        print("here")
    def configure(self,event):
        self.textbox.see(tk.END)
    def runable(self):
        while True:
            self.old = self.new
            self.new = EBLib.getid(self.server,self.port)
            #print(self.old,self.new)
            if self.new != self.old:
                self.refresh()
                print("refreshed")
                time.sleep(2)
    def refresh(self):
        self.richthread = threading.Thread(target=self.richimg)
        self.highlightthread = threading.Thread(target=self.highlight)
        self.textbox.config(state=tk.NORMAL)
        self.textbox.see(tk.END)
        self.url = self.server + ":" + self.port + "?get"
        self.incommingdata = requests.get(self.url)
        self.downloadedtext = self.incommingdata.text
        self.lines = self.downloadedtext.split("\n")
        print(self.lines)
        self.lines.reverse()
        self.imglist = {}
        self.imgdata = {}

        self.linklist = {}
        self.linenum = len(self.lines)
        print(self.linenum)
        self.imgcount = 0

        for self.currentline in self.lines:
            self.linenum -= 1
            #print(self.currentline)
            #print(self.linenum)
            try:
                if self.currentline[0] == "i" and self.currentline[1] =="m" and self.currentline[2] =="g" and self.currentline[3] == "|":
                    if self.imgcount != 5:
                        self.imglist[self.linenum] = self.currentline[4:]
                        self.imgcount += 1
                if self.currentline[0] == "|" and self.currentline[1] == "l":
                    self.linklist[self.linenum] = self.currentline[6:]
            except:
                pass

        self.textbox.delete('1.0', tk.END)
        self.textbox.insert('1.0', self.downloadedtext)
        print(self.linklist,self.imglist)
        self.richthread.start()
        self.highlightthread.start()
        self.richlink()
        # Old rich text code was here before multithreaded

        self.textbox.config(state=tk.DISABLED)
        self.richthread.join()
        self.highlightthread.join()
        print("here")

    def highlight(self):
        self.textbox.tag_configure("blue", foreground="#00c0FF")
        self.textbox.tag_configure("red", foreground="#ff0000")
        self.textbox.tag_configure("green", foreground="#00ff00")
        self.textbox.highlight_pattern("/.*:", "blue", regexp=True, start="end-25l")
        self.textbox.highlight_pattern("=.*:", "green", regexp=True, start="end-25l")
        self.textbox.highlight_pattern("-.*:", "red", regexp=True, start="end-25l")
        self.textbox.see(tk.END)

    def richimg(self):
        self.imagenum = 0
        #topbar.statuschange("")
        for self.imgrender in self.imglist:
            topbar.pro.pack(side=tk.RIGHT)
            self.imagenum += 1
            #TODO Make each image load individualy from eachother

            #self.textbox.see(tk.END)
            self.prepstring = str(self.imgrender) + ".0"
            topbar.pro.step(10)
            topbar.statuschange("Loading Image " + str(self.imagenum) +  "/" +str(self.imageback) + "   ")

            self.imgdata[self.imgrender] = EBLib.ImageChatFrame(self.textbox,self.imglist[self.imgrender],self.server,self.port)
            self.textbox.window_create(self.prepstring, window=self.imgdata[self.imgrender])
            print(self.imgrender,self.imglist[self.imgrender])
            self.textbox.see(tk.END)
            topbar.pro.step(10)
            if self.imagenum == self.imageback:
                topbar.statuschange("Ready   ")
                topbar.pro.pack_forget()

    def richlink(self):
        for self.linkrender in self.linklist:
            self.outstring = self.linklist[self.linkrender]
            self.linegood = str(self.linkrender+1) + ".0"
            self.lineclear = str(self.linkrender+1) + ".999999999"
            self.textbox.delete(self.linegood,self.lineclear)
            print(self.linegood,self.outstring)
            self.textbox.insert(self.linegood, self.outstring, self.hypeman.add(self.outstring))
            self.textbox.see(tk.END)


class EBClient(tk.Frame):
    def __init__(self,parent,server,port,username,imgback,*args,**kwargs):
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.server = server
        self.username = username
        self.port = port
        self.imgback = imgback
        self.chatbox = ChatReadOut(self,self.server,self.port,('Biome', 13),self.imgback)
        self.chatbox.pack(fill=tk.BOTH)
        self.ebox = TextInputBlock(self,self.server,self.port,self.username,font = ('Biome', 13))
        self.ebox.pack(expand=True,fill=tk.BOTH)

class MenuAdd(tk.Frame):
    def __init__(self,parent,server,port,clientversion,*args,**kwargs):
        #s = ttk.Style()
        #s.theme_use("")

        self.clientversion = clientversion
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.server = server
        self.port = port
        self.mainbar = EBLib.TopBar(self.parent)
        self.mainbar.pack(fill='x', side=tk.TOP)
        self.statbar = EBLib.TopBar(self.parent)
        self.statbar.pack(fill='x',side = tk.BOTTOM)
        # MENUBAR CODE //todo: Make OOP
        self.FileMenu = tk.Menu(root, background='gray10', foreground='white',
                                activebackground='#004c99', activeforeground='white',
                                tearoff=0)
        self.FileDrop = tk.Label(self.mainbar, text="File", bg="gray10", fg="white")

        self.FileDrop.pack(side=tk.LEFT)
        self.FileDrop.bind("<Button-1>",self.do_file_popup)
        self.spacer = tk.Label(self.statbar,text="    ",bg="gray10")
        self.spacer.pack(side=tk.RIGHT)
        self.pro = ttk.Progressbar(self.statbar,length=200)
        self.pro.pack(side=tk.RIGHT)
        self.status = tk.Label(self.statbar, text="Ready   ",bg="gray10",fg="white")
        self.status.pack(side=tk.LEFT)

    def statuschange(self,text):
        self.text = text
        self.status.config(text=self.text)
    def linker(self,ebcontroller):
        self.ebcontroller=ebcontroller
        self.FileMenu.add_command(label="Refresh", command=self.ebcontroller.chatbox.trigger)
        self.FileMenu.add_command(label="About",command=self.about)
    def do_file_popup(self,event):
        # display the popup menu
        try:
            self.FileMenu.tk_popup(event.x_root, event.y_root + 15, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.FileMenu.grab_release()

    def about(self):
        print("abouted")
        try:
            self.aurl = self.server + ":" + self.port + "/ver"
            self.temp = requests.get(self.aurl)
            self.serverversion = self.temp.text
            print(self.serverversion)
        except:
            self.serverversion = "Error connecting to server"

        messagebox.showinfo(title="About", message="ChatNoise -> A chat client/protocol for the people\n"
                                                   "Developed By: InventorXtreme\n"
                                                   "Client Version " + self.clientversion + ""
                                                                                       " using Tkinter GUI\n"
                                                                                       "Server Version: " + self.serverversion)


if __name__ == "__main__":
    server = "https://inventorxtreme19.pythonanywhere.com"
    username = "/Alex"
    port = "443"
    clientversion = "- 0.10.0"
    windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    root.title("Electric Boogaloo Chat Noise Client" + clientversion)
    topbar = MenuAdd(root, server, port,clientversion)
    main = EBClient(root,server,port,username,5)
    topbar.linker(main)
    rethread = threading.Thread(target=main.chatbox.runable,daemon=True)
    rethread.start()
    main.pack(fill=tk.BOTH)
    root.bind('<Return>', main.ebox.send)
    root.mainloop()