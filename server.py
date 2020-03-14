from flask import Flask, render_template, request, jsonify
import socket
import configparser
import threading
import os
from os import scandir

uiFolder = ""
modsFolder = ""
port = ""
IPAddr = ""
configData = None

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
    global meta
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

def Browser(port, IPAddr):
    import webbrowser

    url = f'http://{IPAddr}:{port}/'
    webbrowser.open_new(url)

def getBrowserData():
    config = getConfig()
    ip = getIP()
    url = f'http://{ip}:{config["port"]}/'
    return url

def getConfig():
    global configData
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
    except:
        print(" - Error in config.ini")

    configData = {
        "autoIP": config['Server']['autoIP'],
        "ip": config['Server']['ip'],
        "port": config['Server']['port'],
        "uiFolder": config['Server']['uiFolder'],
        "debug": config['Server']['debug']
    }
    return configData

def getIP():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return IPAddr

def runServer():
    global uiFolder
    global port
    global IPAddr

    config = getConfig()
    if (config['autoIP'] == "True" or config['autoIP'] == "yes" or config['autoIP'] == "true"):
        IPAddr = getIP()
    else:
        IPAddr = config['ip']

    port = config['port']
    uiFolder = config['uiFolder']

    if(config['debug'] == "True" or config['debug'] == "yes"):
        debug = True
    else:
        debug = False


    #app.config['STATIC_FOLDER'] = "www"
    app.debug = debug
    url = f'http://{IPAddr}:{port}/'
    try:

        app.run(host=IPAddr, port=port)

    except:
        print(" - Server won't start")
    try:
        os.popen(f"netsh advfirewall firewall add rule name=PortableController dir=in action=allow protocol=TCP localport={port}")
    except:
        print(" - Firewall can't be open")



