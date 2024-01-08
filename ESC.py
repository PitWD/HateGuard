import os
import sys, termios, fcntl      # GetKey

class ForeGroundColor:
    Black = 30
    Red = 31
    Green = 32
    Yellow = 33
    Blue = 34
    Magenta = 35
    Cyan = 36
    LightGray = 37
    DarkGray = 90
    LightRed = 91
    LightGreen = 92
    LightYellow = 93
    LightBlue = 94
    LightMagenta = 95
    LightCyan = 96
    White = 97

class BackGroundColor:
    Black = 40
    Red = 41
    Green = 42
    Yellow = 43
    Blue = 44
    Magenta = 45
    Cyan = 46
    LightGray = 47
    DarkGray = 100
    LightRed = 101
    LightGreen = 102
    LightYellow = 103
    LightBlue = 104
    LightMagenta = 105
    LightCyan = 106
    White = 107

# Classes for solarized color scheme
class Solarized16:
    Base03 = 30  # Schwarz
    Base02 = 40  # Hintergrundfarbe Schwarz
    Base01 = 32  # Grün
    Base00 = 33  # Gelb
    Base0 = 34   # Blau
    Base1 = 36   # Cyan
    Base2 = 37   # Hellgrau
    Base3 = 97   # Weiß
    Yellow = 33  # Gelb
    Orange = 31  # Rot
    Red = 31     # Rot
    Magenta = 35 # Magenta
    Violet = 35  # Magenta
    Blue = 34    # Blau
    Cyan = 36    # Cyan
    Green = 32   # Grün



def GetKey():
    # from: https://stackoverflow.com/questions/71801157/detect-key-press-in-python-without-running-as-root-and-without-blockingioerror
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:
        while True:
            try:
                c = sys.stdin.read(1)
                if c:
                    return c
                else:
                    return 0
                
            except IOError: pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

def BreakLines(text, pos):
    # Split a string into multiple lines, each with a maximum length of 'pos'
    lines = []
    doubleLF = 0
    for line in text.splitlines():
        while len(line) > pos:
            space_index = line.rfind(' ', 0, pos)
            if space_index == -1:  # If no space found before the Xth character
                space_index = pos  # Break at the 60th character anyway
            lines.append(line[:space_index].rstrip())
            line = line[space_index:].lstrip()
        if line:  # Add any remaining part of the line
            lines.append(line)
            doubleLF = 0
        else:   # simulate original LineFeed
            if not doubleLF:    # prevent multiple LF
                lines.append(" ")
                doubleLF = 1
    return '\n'.join(lines)

def PrintLines(text, offset):
    # Print a string, line for line, with a given offset
    for line in text.splitlines():
        CursorRight(offset)
        print(line)

def CursorSave():
    print("\0337", end="", flush=True)

def CursorRestore():
    print("\0338", end="", flush=True)

def CursorDown(y):
    print("\x1B[" + str(y) + "B", end="", flush=True)

def CursorRight(x):
    print("\x1B[" + str(x) + "C", end="", flush=True)

def CursorLeft(x):
    print("\x1B[" + str(x) + "D", end="", flush=True)

def CursorUp(y):
    print("\x1B[" + str(y) + "A", end="", flush=True)

def CursorMoveX(x):
    if x > 0:
        CursorRight(x)
    elif x < 0:
        CursorLeft(x * -1)

def CursorMoveY(y):
    if y > 0:
        CursorUp(y)
    elif y < 0:
        CursorDown(y * -1)

def CursorMoveXY(x, y):
    CursorMoveX(x)
    CursorMoveY(y)

def CursorAbs(x, y):
    print("\x1B[" + str(y) + ";" + str(x) + "H", end="", flush=True)

def CLS():
    os.system('cls' if os.name == 'nt' else 'clear')    
    # print("\x1B[2J", end="", flush=True)

def TxtBold(set):
    if set:
        print("\x1B[1m", end="", flush=True)
    else:
        print("\x1B[22m", end="", flush=True)

def ResetForeGround():
    print("\x1B[39m", end="", flush=True)

def ResetBackGround():
    print("\x1B[49m", end="", flush=True)

def ResetForeBack():
    ResetForeGround()
    ResetBackGround()

def SetForeGround(c):
    if not ((c > 29 and c < 38) or (c > 89 and c < 98)):
        ResetForeGround()
    else:
        print("\x1B[" + str(c) + "m", end="", flush=True)

def SetBackGround(c):
    if not ((c > 39 and c < 48) or (c > 99 and c < 108)):
        ResetBackGround()
    else:
        print("\x1B[" + str(c) + "m", end="", flush=True)

def SetForeBack(fc, bc):
    SetForeGround(fc)
    SetBackGround(bc)
