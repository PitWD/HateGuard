import ESC
import time
import sys
import os

def PrintMenuPos(key, text, keyColor = ESC.Solarized16.Orange, txtColor = ESC.Solarized16.Base02, offset = 4):
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
