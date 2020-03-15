from flask import Flask, render_template, request, jsonify
import sys
import socket
import configparser
import threading
import os
from mods import keyboard

uiFolder = ""
modsFolder = ""
port = ""
IPAddr = ""
configData = None

app = Flask(__name__, static_folder="www")

@app.route('/')
def index():
    folder = scanDir()
    config = getConfig()
    ip = getIP()
    html = f'''
            <html>
                <head>
                    <link rel="shortcut icon" type="image/x-icon" href="http://{ip}:{config["port"]}/www/favicon.ico">
                    <link rel="stylesheet" type="text/css" href="http://{ip}:{config["port"]}/www/style.css">
                    <script src="http://{ip}:{config["port"]}/www/style.js"></script>
                </head>
                <body>
                    <h1 align="center">// Portable Controller</h1>
                    <table class="tg">
                        <tr>
                            <th class="tg-baqh">Logo</th>
                            <th class="tg-0lax">Game</th>
                            <th class="tg-0lax">GameVersion</th>
                            <th class="tg-0lax">Description</th>
                            <th class="tg-0lax">Version</th>
                            <th class="tg-0lax">Author</th>
                            <th class="tg-0lax">Release</th>
                            <th class="tg-0lax">Devices</th>
                            <th class="tg-0lax">Link</th>
                        </tr>'''


    for dir in folder:
        html += "<tr>"
        metaData = readMeta(dir)
        html += f'''<td class="tg-0lax"><a href="http://{ip}:{config["port"]}/www/{dir}/index.html"><img src="http://{ip}:{config["port"]}/www/{dir}/logo.png" width="64px"> </td>
                    <td class="tg-0lax">{metaData["game"]}</td>
                    <td class="tg-0lax">{metaData["gameversion"]}</td>
                    <td class="tg-0lax">{metaData["description"]}</td>
                    <td class="tg-0lax">{metaData["version"]}</td>
                    <td class="tg-0lax">{metaData["author"]}</td>
                    <td class="tg-0lax">{metaData["release"]}</td>
                    <td class="tg-0lax">{metaData["devices"]}</td>
                    <td class="tg-0lax"><a href="{metaData["url"]}" target="_blank">Link</a></td></tr>'''
    html += "</table>"
    html += '<br><br><footer><a class="link" align="center" href="https://portable-controller.de" target="_blank">TJ 2020 - Portable-Controller.de</a></footer></body></html>'
    return html

@app.route('/key', methods=['POST'])
def key():
    type = request.form.get("type")
    key = request.form.get("key")
    counter = request.form.get("counter")
    timer = request.form.get("timer")
    counter = int(counter)
    timer = int(timer)
    try:
        th = threading.Thread(target=keyboard.button, args=(key, counter,timer))
        th.start()
    except:
        print ("Error: unable to start thread")

    return "success"

@app.route('/text', methods=['POST'])
def text():
    chatOpen = request.form.get("chatOpen")
    chatText = request.form.get("chatText")
    chatSend = request.form.get("chatSend")
    try:
        th = threading.Thread(target=keyboard.text, args=(chatOpen, chatText, chatSend))
        th.start()
        return "success"
    except:
        print ("Error: unable to start thread")
        return "failed"

def scanDir():
    dir = "www"

    listDir = []
    obj = os.scandir(dir)
    for entry in obj:
        if entry.is_dir():
             listDir.append(entry.name)


    return listDir

def readMeta(path):
    metaPath = f"www/{path}/meta.ini"
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

def Browser(url, port = 0, IPAddr = ""):
    import webbrowser

    if url == "":
        url = f'http://{IPAddr}:{port}/'
        webbrowser.open_new(url)
    else:
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



