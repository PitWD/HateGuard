import ESC
import time
import sys
import os

def PrintMenuPos(key, text, keyColor=None, txtColor=None, offset=None):
    
    if keyColor is None:
        keyColor = ESC.Solarized16.Orange
    if txtColor is None:
        txtColor = ESC.Solarized16.Base1
    if offset is None:
        offset = 4
    
    ESC.CursorRight(offset)
    ESC.SetForeGround(keyColor)  
    ESC.TxtBold(True)   
    print(str(key), end="")
    ESC.TxtBold(False)
    print(")", end="")
    ESC.SetForeGround(ESC.Solarized16.Base2)
    print(" = ", end="")
    ESC.SetForeGround(txtColor)
    print(text, flush=True)
    ESC.ResetForeGround()


def PrintRainbow(txt):
    color =[31, 91, 33, 32, 36, 34, 95] # Solarized Red, Orange, Yellow, Green, Cyan, Blue, Violet
    rest = 0
    length = len(txt)
    parts = 7

    if length < parts:
        parts = length
    else:
        rest = length % parts

    chars_per_part = length // parts
    for i in range(parts):
        ESC.SetForeGround(color[i])
        if i != 0 and rest != 0:
            # No rest on 1st color
            print(txt[:chars_per_part + 1], end="")
            txt = txt[chars_per_part + 1:]
            rest -= 1
        else:
            print(txt[:chars_per_part], end="")
            txt = txt[chars_per_part:] 

    ESC.ResetForeGround()
