import server
import sys
import multiprocessing as mp
import PySimpleGUI as sg
import datetime
import os
import time
serverRunning = False
serverD =  None

def getTime():
    now = datetime.datetime.now()
    return now.strftime('%H:%M:%S')

def pcServer():
    global serverRunning
    global serverD

    if serverRunning == False:
        try:
            serverD = mp.Process(target=server.runServer)
            serverD.daemon = True
            serverD.start()

            serverRunning = True
            print(getTime() + " - Server started")
        except:
            print(getTime() + " - Error: Server won't start")
    else:
        try:
            serverD.terminate()
            serverRunning = False
            print(getTime() + " - Server stopped")
        except:
            print(getTime() + " - Error: Server won't stop")
            # self.text.setText("PortableController won't stop")


def GUI():

    sg.theme('DarkBlue1')  # please make your windows colorful

    layout = [[sg.Text('Portable Controller')],
              [sg.Output(background_color='#F7F3EC', text_color='black', size=(35, 7))],
              [sg.Button("Server Start", key='-BUTTON-'), sg.Open("Open Browser"), sg.Exit()]]

    window = sg.Window('Portable Controller', layout, no_titlebar=True, size=(300, 200), resizable=False,
                       keep_on_top=False, alpha_channel=.95, grab_anywhere=True)

    while True:  # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        if event == '-BUTTON-':
            if serverRunning == False:
                pcServer()
                window['-BUTTON-'].Update("Server Stop")

                print(server.getBrowserData())
            else:
                pcServer()
                window['-BUTTON-'].Update("Server Start")


        elif event == 'Open Browser':
            config = server.getConfig()
            ip = server.getIP()
            server.Browser(config["port"], ip)
    window.Close()



if __name__ == '__main__':
    GUI()
    print('Exiting Program')