import keyboard
import time

def button(key, counter=1, timer=0):

    if(counter == 1):
        keyboard.press_and_release(key)
    else:
        for n in range(1, counter, 1):
            keyboard.press_and_release(key)
            time.sleep(timer)


    return True

def text(chatOpen, chatText, chatSend):
    keyboard.press_and_release(chatOpen)
    text = map(lambda x: x, chatText)

    for char in text:
        if char == " " or char == "":
            keyboard.press_and_release("space")
        else:
            keyboard.press_and_release(char)
        print(char)
    keyboard.press_and_release(chatSend)
    return "success"