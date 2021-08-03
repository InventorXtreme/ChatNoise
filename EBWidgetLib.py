import os
import webbrowser
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import urllib
import requests
import imghdr
import socket
import threading
import pyaudio
import struct
import math
#from browser import *
import sys
from tkinter import messagebox
try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
except AttributeError:
    base_path = os.path.abspath(".")

# Python 3.8 things:
try:
    with os.add_dll_directory(os.path.join(base_path, "VLC")):
        import vlc
except:
    print("linux mode:tm:")
    import vlc

import pafy
import time
from multiprocessing import Process, Value, Array
#Todo make a status bar that can be placed at the bottom of the root window to show progress of image loading
#Todo: Make a scrollbar on text widget

class Screen(tk.Frame):
    def __init__(self, parent, yturl, *args, **kwargs):
        tk.Frame.__init__(self, parent, bg = 'black')
        self.settings = { # Inizialazing dictionary settings
            "width" : 300,
            "height" : 225
        }
        self.parent = parent
        self.settings.update(kwargs) # Changing the default settings
        # Open the video source |temporary
        self.video_source =  "https://www.youtube.com/watch?v=b8HO6hba9ZE"
        self.yturl = yturl
        # Canvas where to draw video output
        self.canvas = tk.Canvas(self, width = self.settings['width'], height = self.settings['height'], bg = "black", highlightthickness = 0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>",self.pause)



    def vidinit(self):
        # Creating VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.vid = pafy.new(self.yturl)
        self.gamer = self.vid.getbest()
        # self.player.play()
        Media = self.instance.media_new(self.gamer.url)
        Media.get_mrl()
        self.player.set_media(Media)
        self.player.set_hwnd(self.GetHandle())
        self.player.set_xwindow(self.GetHandle())
        self.player.play()
        self.player.video_set_mouse_input(False)
        self.player.video_set_key_input(False)
        self.progupdatethread = threading.Thread(target=self.updateprogress)
        self.progupdatethread.start()



    def GetHandle(self):
        # Getting frame ID
        return self.winfo_id()


    def pause(self,no):
        self.parent.toggle()
        #
        # print("help")
        # #print(vlc.libvlc_media_player_get_position(self.player))
        #
        #
        # self.player.pause()
        # # self.progupdatethread = threading.Thread(target=self.updateprogress)
        # # self.progupdatethread.start()
    def updateprogress(self):
        while True:
            if self.player.is_playing() == 1:
                self.parent.progset(vlc.libvlc_media_player_get_position(self.player))
            time.sleep(0.016666)





class YoutubeEmbed(tk.Frame):
    def __init__(self,parent,imgfilename,line,*args,**kwargs):
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.filename = imgfilename
        # self.server = server
        # self.port = port
        self.parent = parent
        self.line = line
        # self.string = "./cimg/cashedimage" + str(self.line)
        # self.url = self.server + ":" + self.port + "/image/" + self.filename
        # urllib.request.urlretrieve(self.url, self.string)
        # self.imgd = Image.open(self.string)
        # self.tkimg = ImageTk.PhotoImage(self.imgd)
        # self.filetype = imghdr.what(self.string, h=None)
        # self.imgd.close()

        self.widget = Screen(self,self.filename)
        #self.widget.play(self.filename)
        print("yteframe")
        self.widget.pack()
        self.widget.bind("<Button-1>",self.toggle)
        #self.length = self.widget.player.get_position()
        #self.length = vlc.libvlc_media_player_get_position(self.widget.player)
        #print(self.length)
        self.state = "ninit"
        s = ttk.Style()
        s.theme_use('alt')
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red',troughcolor='gray10')
        s.configure('my.TButton', font=("webdings", 10), padding=-3)

        self.ctrlframe = tk.Frame(self,bg="gray10")

        self.progvar = tk.IntVar()
        self.progressbar = self.aliveness = ttk.Progressbar(self.ctrlframe, orient="horizontal", length=280, mode="determinate",variable=self.progvar,style="red.Horizontal.TProgressbar")
        self.progressbar.pack(side=tk.RIGHT)
        self.progressbar.bind('<Button-1>',self.setpos)
        self.pausebutton = ttk.Button(self.ctrlframe,command=self.toggle,text="4",style='my.TButton',width=1)
        self.pausebutton.pack(side=tk.LEFT)
        self.ctrlframe.pack()
    def toggle(self):
        if self.state == "ninit":
            self.widget.vidinit()
            self.state = "playing"
            self.pausebutton.config(text=";")
            return
        if self.state == "playing" or self.state == "paused":
            self.widget.player.pause()
            if self.state == "playing":
                self.state = "paused"
                self.pausebutton.config(text="4")
            else:
                self.state = "playing"
                self.pausebutton.config(text=";")

        #print(self.state)
    def setpos(self,event):
        #print(event.x/300)
        vlc.libvlc_media_player_set_position(self.widget.player,event.x/280)
        self.progvar.set(vlc.libvlc_media_player_get_position(self.widget.player)*100)


    def progset(self,percentplayed):
        #print(percentplayed)
        self.progvar.set(percentplayed*100)


class ImageChatFrame(tk.Frame):
    def __init__(self,parent,imgfilename,server,port,line,*args,**kwargs):
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.filename = imgfilename
        self.server = server
        self.port = port
        self.parent = parent
        self.line = line
        self.string = "./cimg/cashedimage" + str(self.line)
        self.url = self.server + ":" + self.port + "/image/" + self.filename
        urllib.request.urlretrieve(self.url, self.string)
        self.imgd = Image.open(self.string)
        self.tkimg = ImageTk.PhotoImage(self.imgd)
        self.filetype = imghdr.what(self.string, h=None)
        self.imgd.close()
        if self.filetype != "gif":
            self.widget = tk.Label(self, image=self.tkimg)
            self.widget.pack()
        else:
            self.widget = AnimatedGIF(self,self.string)
            self.widget.start_animation()
            self.widget.pack()



class AudioMan(tk.Frame):
    def __init__(self,parent,audioclient,*args,**kwargs):
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.incall = False
        self.parent = parent
        self.audioclient = audioclient
        self.joinbutton = tk.Button(self,text="Connect",command=self.button,bg="gray10",fg="white")
        self.speaking = False
        self.infostringdata=audioclient.target_ip + ":" + str(audioclient.target_port)
        self.infostring = tk.Label(self,text=self.infostringdata,bg="gray10",fg="white")
        self.joinbutton.pack(side=tk.LEFT)
        self.infostring.pack(side=tk.LEFT)
    def button(self):
        if self.incall == False:
            if self.audioclient.connect() == 0:
                self.joinbutton.config(text="Disconnect")
                self.update_thread = threading.Thread(target=self.update)
                self.update_thread.daemon = True
                self.update_thread.start()
                self.incall = True
            else:
                messagebox.showerror("AudioMan", "Error connecting to server")
        else:

            try:
                self.audioclient.disconnect()
            except TypeError:
                pass
            self.joinbutton.config(text="Connect")
            self.incall = False
    def update(self):
        while True:
            try:
                if self.audioclient.decibel > -43:
                    self.speaking = True
                    self.infostring.config(fg="green")
                else:
                    self.speaking = False
                    self.infostring.config(fg="white")
            except:
                pass
            if self.incall == False:
                break


class Client:
    def __init__(self,server,port,parrent):
        self.parrent = parrent
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.target_ip = server
        self.target_port = int(port)
        self.chunk_size = 1024  # 512
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 20000
        self.decibel = 0
        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.connected = False


    def connect(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.s.connect((self.target_ip, self.target_port))
            self.playing_stream = self.p.open(format=self.audio_format, channels=self.channels, rate=self.rate,
                                              output=True,
                                              frames_per_buffer=self.chunk_size)
            self.recording_stream = self.p.open(format=self.audio_format, channels=self.channels, rate=self.rate,
                                                input=True,
                                                frames_per_buffer=self.chunk_size)

            print("Connected to Server")

            # start threads
            self.connected = True
            self.receive_thread = threading.Thread(target=self.receive_server_data).start()
            self.send_thread = threading.Thread(target=self.send_data_to_server).start()

            return 0

        except:
            print("Couldn't connect to server")
            return 1



    def receive_server_data(self):
        while self.connected:
            try:
                # TODO: GET PERF ON RPI4
                #self.parrent.update_idletasks()
                #self.parrent.update()
                self.data = self.s.recv(self.chunk_size)

                self.playing_stream.write(self.data)


            except:
                pass


    def send_data_to_server(self):
        while self.connected:

            #try:
            self.data = self.recording_stream.read(self.chunk_size)
            vol = self.rms(self.data)
            self.decibel = 20 * math.log10(vol)
            print(self.decibel)


            if self.decibel > -43:
                self.s.sendall(self.data)

            #except:
            #    pass
    def disconnect(self):
        self.connected = False
        try:
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
            self.send_thread.join()
            self.receive_thread.join()
        except:
            pass

    def rms(self,data):
        count = len(data) / 2
        format = "%dh" % (count)
        shorts = struct.unpack(format, data)
        sum_squares = 0.0
        for sample in shorts:
            n = sample * (1.0 / 32768)
            sum_squares += n * n
        return math.sqrt(sum_squares / count)





def getid(server,port):
    idurl = server + ":" + port + "/messageid/"
    x = requests.get(idurl)
    res = x.text
    out = res
    return out
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
        for tag in self.text.tag_names(tk.CURRENT):
            if tag[:6] == "hyper-":
                webbrowser.open(self.links[tag])
                return

class AnimatedGIF(tk.Label, object):
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
        try:
            self.configure(image=self._frames[self._loc])
        except:
            pass

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

class CustomText(tk.Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

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

        count = tk.IntVar()
        indexlist = []
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

class ChannelListBox(tk.Frame):
    def __init__(self,parent,rootobj,*args,**kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.searchvar = tk.StringVar(value="Search")
        self.searchvar.trace("w", self.updatelistbox)
        self.searchbar = tk.Entry(self, textvariable=self.searchvar, bg="gray10", fg="white")
        self.searchbar.bind('<Button-1>', self.clearentry)
        self.searchbar.pack(fill=tk.X)
        self.channellistbox = tk.Listbox(self,bg="gray10",fg="white")
        self.channellistbox.pack(fill=tk.BOTH,expand=1)
        self.channellistbox.bind('<<ListboxSelect>>',self.changechan)
        self.rootobj = rootobj



    def loadlist(self):
        self.textfile = open("channellist.txt","r+")
        self.channellist = self.textfile.read().splitlines()
        self.channellist.append("Main Channel")
        for self.channelvalue in self.channellist:
            self.channellistbox.insert(tk.END,self.channelvalue)

        self.textfile.close()

    def updatelistbox(self,*args):
        self.searchterm=self.searchvar.get()
        self.channellistbox.delete(0,tk.END)

        try:
            for self.searchitem in self.channellist:
                if self.searchterm.lower() in self.searchitem.lower():
                    self.channellistbox.insert(tk.END,self.searchitem)
        except:
            pass
    def clearentry(self,event):
        print(event.widget)
        #print(root.focus_get())
        if event.widget != self.parent.focus_get():
            self.searchbar.delete(0,tk.END)

    def changechan(self,*args):
        print(self.channellistbox.get(self.channellistbox.curselection()))
        if self.channellistbox.get(self.channellistbox.curselection()) == "Main Channel":
            self.rootobj.changechan("")
        else:
            self.rootobj.changechan(self.channellistbox.get(self.channellistbox.curselection()))
        #self.rootobj.chatbox.trigger()
        print(self.channellistbox.get(self.channellistbox.curselection()))
