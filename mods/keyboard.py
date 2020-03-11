import keyboard
import time

def button(key, counter=1, timer=0):

    if(counter == 1):
        print("Press")
        keyboard.press_and_release(key)
    else:
        for n in range(1, counter, 1):
            keyboard.press_and_release(key)
            time.sleep(timer)


    return True