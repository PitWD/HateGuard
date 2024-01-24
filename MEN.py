import ESC
import time
import sys
import os

def PrintRating(rating):
    if rating == 1 or rating == '1':
        ESC.SetForeGround(ESC.Solarized16.Green)
        print("OK", end="")
    elif rating == 2 or rating == '2':
        ESC.SetForeGround(ESC.Solarized16.Orange)
        print("WARNING", end="")
    elif rating == 3 or rating == '3':
        ESC.SetForeGround(ESC.Solarized16.Red)
        print("CRITICAL", end="")
    else:
        ESC.SetForeGround(ESC.Solarized16.Blue)
        print("unrated", end="")

def GetRatingColor(rating):

    if rating == 1 or rating == '1':
        return ESC.Solarized16.Green
    elif rating == 2 or rating == '2':
        return ESC.Solarized16.Orange
    elif rating == 3 or rating == '3':
        return ESC.Solarized16.Red
    else:
        return ESC.Solarized16.Blue

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

def PrintInfoPos(key, text, keyColor=None, txtColor=None, offset=None, end=None):
    
    if keyColor is None:
        keyColor = ESC.Solarized16.Base00
    if txtColor is None:
        txtColor = ESC.Solarized16.Base1
    if offset is None:
        offset = 4
    if end is None:
        end = "\n"
    
    ESC.CursorRight(offset)
    ESC.SetForeGround(keyColor)  
    print(str(key), end="")
    ESC.SetForeGround(ESC.Solarized16.Base2)
    print(": ", end="")
    ESC.SetForeGround(txtColor)
    print(text, flush=True, end=end)
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
