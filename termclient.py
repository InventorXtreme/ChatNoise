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
import base64
import os
from tkinter import filedialog

try:
    config = pickle.load(open("config.p", "rb"))
    user = config["username"]
    print("config loaded")
    print(user)
except:
    print("CONFIG ERROR: SETTING UP")
    config = {"username":"Guestsadf"}
    pickle.dump(config, open("config.p","wb+"))

def loadb64image():
    base64_img = input("Input Image Data to Decode ")
    fileex = input("File Type (Ex: .jpg or .png ")
    base64_img_bytes = base64_img.encode('utf-8')
    filename = "decoded_data" + fileex
    with open(filename, 'wb') as file_to_save:
        decoded_image_data = base64.decodebytes(base64_img_bytes)
        file_to_save.write(decoded_image_data)
    os.system('decoded_image.png')


def encodeb64image():
    filename = filedialog.askopenfilename()
    if filename != "":
        with open(filename, 'rb') as binary_file:
            binary_file_data = binary_file.read()
            base64_encoded_data = base64.b64encode(binary_file_data)
            base64_message = base64_encoded_data.decode('utf-8')

            # chatbox.insert(END,base64_message)
        with open("out.txt","w+") as outfile:
            outfile.write(base64_message)
        fileopen = threading.Thread(target=openfile(), args=(1,), daemon=True)
        fileopen.start()


def openfile():
    os.system("out.txt")
def sync():
    send()
def send_clip():
    send(root.clipboard_get())

def send(senddata):
    outline = user + ": " + senddata

    out = "http://127.0.0.1:69?send=" + outline
    temp = requests.get(out)

def setupdate():
    global updategood
    updategood = not updategood

def sendread():
    try:
        send(chatbox.get())
    except requests.exceptions.ConnectionError:
        tkinter.messagebox.showerror(title="NetError", message="Connection Error sending data to server")



def update_display():
    try:
        down = requests.get("http://127.0.0.1:69?get")
    except requests.exceptions.ConnectionError:
        return "Error Connecting to server"
    x = down.text
    with open("chatlogclient.txt", "w+") as file:
        file.write(x)
    with open("chatlogclient.txt", 'r') as fin:
        return fin.read()

while True:
    command = input("])}")
    if command == "send":
        out = input("What to Send? ")
        send(out)
    elif command == "re":
        print(update_display())
    elif command == "exit":
        break
    elif command == "encode":
        encodeb64image()
    elif command == "decode":
        loadb64image()