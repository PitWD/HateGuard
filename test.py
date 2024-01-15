import ESC
import os
import time

ESC.CLS()

os.system('stty -echo')

while True:
    pressedKey = ESC.GetKey()
    if pressedKey != "":
        print("You pressed: " + pressedKey + ", UTF value of first char: " + str(ord(pressedKey[0])))
        if pressedKey == "q":
            break
    else:
        time.sleep(0.05)    

ESC.edlin("Schaun mer mal...")

os.system('stty echo')