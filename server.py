from flask import Flask, render_template, request, jsonify
import socket
import configparser
import threading
from os import scandir

uiFolder = ""
modsFolder = ""

app = Flask(__name__, static_folder="www")

@app.route('/')
def index():
    return "hallo"

@app.route('/key', methods=['POST'])
def key():
    from mods import keyboard
    type = request.form.get("type")
    key = request.form.get("key")
    counter = request.form.get("counter")
    timer = request.form.get("timer")
    counter = int(counter)
    timer = int(timer)
    #print(request.form.get("counter"))
    try:
        th = threading.Thread(target=keyboard.button, args=(key, counter,timer))
        th.start()
    except:
        print ("Error: unable to start thread")

    return "success"

def scanDir():
    global uiFolder
    dir = uiFolder
    print (dir)
    subdir = []
    for root, dirs, files in os.walk(top, topdown=False):
        for name in dirs:
            subdir.append(os.path.join(root, name))


    return subdir

def readConfig(path):
    global uiFolder

    metaPath = f"{uiFolder}/{path}/meta.ini"
    print (metaPath)
    config = configparser.ConfigParser()
    config.read(metaPath)
    meta = {
        "author": config['Info']['author'],
        "release": config['Info']['release'],
        "version": config['Info']['version'],
        "game": config['Info']['game'],
        "gameversion": config['Info']['gameversion'],
        "description": config['Info']['description'],
        "url": config['Info']['url'],
        "devices": config['Info']['devices']
    }
    return meta
def runServer():
    global uiFolder
    config = configparser.ConfigParser()
    config.read('config.ini')
    if (config['Server']['autoIP'] == "True" or config['Server']['autoIP'] == "yes" or config['Server']['autoIP'] == "true"):
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
    else:
        IPAddr = config['Server']['ip']

    port = config['Server']['port']

    uiFolder = config['Server']['uiFolder']
    if(config['Server']['debug'] == "True" or config['Server']['debug'] == "yes"):
        debug = True
    else:
        debug = False


    #app.config['STATIC_FOLDER'] = "www"
    app.debug = debug
    app.run(host=IPAddr, port=port)

