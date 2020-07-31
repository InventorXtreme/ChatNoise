import flask
from flask import request, Response
import requests
from flask import Flask, request, redirect, send_file
from werkzeug.utils import secure_filename
import os
import imghdr
servversion = "S0.3a"
app = flask.Flask(__name__)
app.config["DEBUG"] = True
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'gif','py','txt'])
UPLOAD_PATH = './image'
app.config['UPLOAD_PATH'] = UPLOAD_PATH
global messageid
messageid = 0
global msgsync
msgsync = 0
global servname
servname = "ERROR TIME"
global syncserver1
syncserver1 = "http://192.168.86.75:69"
global syncname1
syncname1 = "MACMACMAC1"

def allowed_file(_file):
    image_type = imghdr.what(None, _file.read())
    return image_type in ALLOWED_EXTENSIONS

@app.route("/ver")
def version():
    return servversion

@app.route('/image/<image_name>', methods=['GET'])
def get_image(image_name):
    try:
        if image_name is not None:
            image_name = secure_filename(image_name)
            image = open(os.path.join(app.config['UPLOAD_PATH'], image_name))
            god_christ_help = ".\image/" + image_name
            return send_file(god_christ_help)
        else:
            return 'error'
    except:
        return send_file("image/404error.png",)

@app.route('/messageid/')
def messageidget():
    return str(messageid)

@app.route('/upimage/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        _file = request.files['file']
        if _file:
            filename = secure_filename(_file.filename)
            # because imghdr.what() reads file to end, must set file's position 0.
            _file.seek(0)
            try:
                _file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            except IOError:
                os.mkdir(app.config['UPLOAD_PATH'])
                _file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

            return redirect('/image/' + filename)
        else:
            return "Upload failed."
    else:
        return '<form action="." method="post" enctype="multipart/form-data"><input type="file" name="file" /><button type="submit">Upload</button></form>'

try:
    chatlogtt = open("chatlog.txt",'a')
    chatlogtt.close()
except FileNotFoundError:
    print("File not accessible")


def send1(senddata):

    outline = "SERVNAME" + ": " + senddata

    out = ""+syncserver1+"?send="+senddata
    # out = "http://127.0.0.1:5000?send=" + outline
    temp = requests.get(out)

def sync():
    global syncname1
    with open('chatlog.txt', 'r') as f:
        synclist = [line.strip() for line in f]
    for x in range(msgsync):
        gamer = synclist[::-1]
        prebound = synclist.pop(-1 )
        outbound = servname +" " + prebound
        if prebound[0:10] != syncname1:
            print(outbound)
            send1(outbound)


@app.route('/', methods=['GET'])
def home():
    global messageid
    global msgsync
    if "send" in request.args:
        if int(request.args['id']) > messageid:
            chatlog = open("chatlog.txt", 'a')
            message = request.args['send']
            vermessage = message + '\n'
            chatlog.write(vermessage)
            chatlog.close()
            messageid += 1
            return "writen"
        else:
            return 'ID ERROR'
    elif "cmd" in request.args:
        if int(request.args['id']) > messageid:
            chatlog = open("chatlog.txt", 'a')
            message = request.args['cmd']
            vermessage = message + '\n'
            if message == "@boom":
                chatlog.write("Reee\n")
            chatlog.write(vermessage)
            chatlog.close()
            messageid += 1
        return "cmd good"

    elif "get" in request.args:
        with open("chatlog.txt",'r') as fin:
            return Response(fin.read(), mimetype='text/plain')
    elif "ret" in request.args:
        sync()
        return "hek"

    else:
        return "no request"

app.run(host = "0.0.0.0", port = 80)