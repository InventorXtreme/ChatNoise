import tkinter as tk
import EBWidgetLib as EBLib
import requests
from ctypes import windll
import threading
import time

class ChatReadOut(tk.Frame):
    def __init__(self,parent,server,port,*args,**kwargs):
        self.server = server
        self.port = port
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.textbox = EBLib.CustomText(self)
        self.hypeman = EBLib.HyperlinkManager(self.textbox)
        self.textbox.pack(fill=tk.BOTH)
    def start(self):
        self.mainthread = threading.Thread(target=self.runable)
        self.mainthread.start()
    def runable(self):
        while True:
            self.url = self.server + ":" + self.port + "?get"
            self.incommingdata = requests.get(self.url)
            self.downloadedtext = self.incommingdata.text
            self.lines = self.downloadedtext.split("\n")
            print(self.lines)
            self.lines.reverse()

            self.linelength  = len(self.lines)

            self.textbox.delete('1.0', tk.END)
            self.textbox.insert('1.0', self.downloadedtext)
            self.textbox.see(tk.END)
            time.sleep(2)







class EBClient(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.server = "https://inventorxtreme19.pythonanywhere.com"
        self.port = "443"
        self.chatbox = ChatReadOut(self,self.server,self.port)
        self.chatbox.pack(fill=tk.BOTH)
        self.chatbox.start()


if __name__ == "__main__":
    root = tk.Tk()
    main = EBClient(root)
    main.pack(fill=tk.BOTH)
    windll.shcore.SetProcessDpiAwareness(1)
    root.mainloop()