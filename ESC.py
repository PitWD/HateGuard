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
    Base02 = 30  # Schwarz
    Red = 31     # Rot
    Green = 32   # Grün
    Yellow = 33  # Gelb
    Blue = 34    # Blau
    Magenta = 35 # Magenta
    Cyan = 36    # Cyan
    Base2 = 37   # Weiß
    Base03 = 90  # brSchwarz
    Orange = 91  # Grün
    Base01 = 92  # Gelb
    Base00 = 93   # Cyan
    Base0 = 94   # Hellgrau
    Violet = 95  # Gelb
    Base1 = 96  # Rot
    Base3 = 97  # Magenta


def KeyToFunction(key):
    escKeys ={
        '\x1bOP': 'F1',
        '\x1bOQ': 'F2',
        '\x1bOR': 'F3',
        '\x1bOS': 'F4',
        '\x1b[15~': 'F5',
        '\x1b[17~': 'F6',
        '\x1b[18~': 'F7',
        '\x1b[19~': 'F8',
        '\x1b[20~': 'F9',
        '\x1b[21~': 'F10',
        '\x1b[23~': 'F11',
        '\x1b[24~': 'F12',
        '\x1b[1;2P': 'Shift-F1',
        '\x1b[1;2Q': 'Shift-F2',
        '\x1b[1;2R': 'Shift-F3',
        '\x1b[1;2S': 'Shift-F4',
        '\x1b[15;2~': 'Shift-F5',
        '\x1b[17;2~': 'Shift-F6',
        '\x1b[18;2~': 'Shift-F7',
        '\x1b[19;2~': 'Shift-F8',
        '\x1b[20;2~': 'Shift-F9',
        '\x1b[21;2~': 'Shift-F10',
        '\x1b[23;2~': 'Shift-F11',
        '\x1b[24;2~': 'Shift-F12',
        '\x1b[1;5P': 'Ctrl-F1',
        '\x1b[1;5Q': 'Ctrl-F2',
        '\x1b[1;5R': 'Ctrl-F3',
        '\x1b[1;5S': 'Ctrl-F4',
        '\x1b[15;5~': 'Ctrl-F5',
        '\x1b[17;5~': 'Ctrl-F6',
        '\x1b[18;5~': 'Ctrl-F7',
        '\x1b[19;5~': 'Ctrl-F8',
        '\x1b[20;5~': 'Ctrl-F9',
        '\x1b[21;5~': 'Ctrl-F10',
        '\x1b[23;5~': 'Ctrl-F11',
        '\x1b[24;5~': 'Ctrl-F12',
        '\x1b[1;6P': 'Ctrl-Shift-F1',
        '\x1b[1;6Q': 'Ctrl-Shift-F2',
        '\x1b[1;6R': 'Ctrl-Shift-F3',
        '\x1b[1;6S': 'Ctrl-Shift-F4',
        '\x1b[15;6~': 'Ctrl-Shift-F5',
        '\x1b[17;6~': 'Ctrl-Shift-F6',
        '\x1b[18;6~': 'Ctrl-Shift-F7',
        '\x1b[19;6~': 'Ctrl-Shift-F8',
        '\x1b[20;6~': 'Ctrl-Shift-F9',
        '\x1b[21;6~': 'Ctrl-Shift-F10',
        '\x1b[23;6~': 'Ctrl-Shift-F11',
        '\x1b[24;6~': 'Ctrl-Shift-F12',
        '\x1b[1;3P': 'Alt-F1',
        '\x1b[1;3Q': 'Alt-F2',
        '\x1b[1;3R': 'Alt-F3',
        '\x1b[1;3S': 'Alt-F4',
        '\x1b[15;3~': 'Alt-F5',
        '\x1b[17;3~': 'Alt-F6',
        '\x1b[18;3~': 'Alt-F7',
        '\x1b[19;3~': 'Alt-F8',
        '\x1b[20;3~': 'Alt-F9',
        '\x1b[21;3~': 'Alt-F10',
        '\x1b[23;3~': 'Alt-F11',
        '\x1b[24;3~': 'Alt-F12',
        '\x1b[1;4P': 'Alt-Shift-F1',
        '\x1b[1;4Q': 'Alt-Shift-F2',
        '\x1b[1;4R': 'Alt-Shift-F3',
        '\x1b[1;4S': 'Alt-Shift-F4',
        '\x1b[15;4~': 'Alt-Shift-F5',
        '\x1b[17;4~': 'Alt-Shift-F6',
        '\x1b[18;4~': 'Alt-Shift-F7',
        '\x1b[19;4~': 'Alt-Shift-F8',
        '\x1b[20;4~': 'Alt-Shift-F9',
        '\x1b[21;4~': 'Alt-Shift-F10',
        '\x1b[23;4~': 'Alt-Shift-F11',
        '\x1b[24;4~': 'Alt-Shift-F12',
        '\x1b[1;7P': 'Alt-Ctrl-F1',
        '\x1b[1;7Q': 'Alt-Ctrl-F2',
        '\x1b[1;7R': 'Alt-Ctrl-F3',
        '\x1b[1;7S': 'Alt-Ctrl-F4',
        '\x1b[15;7~': 'Alt-Ctrl-F5',
        '\x1b[17;7~': 'Alt-Ctrl-F6',
        '\x1b[18;7~': 'Alt-Ctrl-F7',
        '\x1b[19;7~': 'Alt-Ctrl-F8',
        '\x1b[20;7~': 'Alt-Ctrl-F9',
        '\x1b[21;7~': 'Alt-Ctrl-F10',
        '\x1b[23;7~': 'Alt-Ctrl-F11',
        '\x1b[24;7~': 'Alt-Ctrl-F12',
        '\x1b[A': 'Up',
        '\x1b[B': 'Down',
        '\x1b[C': 'Right',
        '\x1b[D': 'Left',
        '\x1b[E': 'Center',
        '\x1b[F': 'End',
        '\x1b[H': 'Home',
        '\x1b[Z': 'Shift-Tab',
        '\x1b[1;2A':'Shift-Up',
        '\x1b[1;2B':'Shift-Down',
        '\x1b[1;2C':'Shift-Right',
        '\x1b[1;2D':'Shift-Left',
        '\x1b[1;2E':'Shift-Center',
        '\x1b[1;2F':'Shift-End',
        '\x1b[1;2H':'Shift-Home',
        '\x1b[1;3A':'Alt-Up',
        '\x1b[1;3B':'Alt-Down',
        '\x1b[1;3C':'Alt-Right',
        '\x1b[1;3D':'Alt-Left',
        '\x1b[1;3E':'Alt-Center',
        '\x1b[1;3F':'Alt-End',
        '\x1b[1;3H':'Alt-Home',
        '\x1b[1;5A':'Ctrl-Up',
        '\x1b[1;5B':'Ctrl-Down',
        '\x1b[1;5C':'Ctrl-Right',
        '\x1b[1;5D':'Ctrl-Left',
        '\x1b[1;5E':'Ctrl-Center',
        '\x1b[1;5F':'Ctrl-End',
        '\x1b[1;5H':'Ctrl-Home',
        '\x7F': 'Back',
        '\x1b[3~': 'Del',
        '\x1b[2~': 'Ins',
        '\x1b[5~': 'PgUp',
        '\x1b[6~': 'PgDn',
        '\x09': 'Tab',
        '\x1b': 'Esc',
        '\x0A': 'Enter',
        '\x0D': 'Enter',
        '\x0D\x0A': 'Enter',
        '\x1b[2;2~': 'Shift-Ins',
        '\x1b[3;2~': 'Shift-Del',
        '\x1b[5;2~': 'Shift-PgUp',
        '\x1b[6;2~': 'Shift-PgDn',
        '\x1b[2;5~': 'Ctrl-Ins',
        '\x1b[3;5~': 'Ctrl-Del',
        '\x1b[5;5~': 'Ctrl-PgUp',
        '\x1b[6;5~': 'Ctrl-PgDn',
        '\x1b[2;3~': 'Alt-Ins',
        '\x1b[3;3~': 'Alt-Del',
        '\x1b[5;3~': 'Alt-PgUp',
        '\x1b[6;3~': 'Alt-PgDn',
        '\x1ba': 'Alt-a',
        '\x1bb': 'Alt-b',
        '\x1bc': 'Alt-c',
        '\x1bd': 'Alt-d',
        '\x1be': 'Alt-e',
        '\x1bf': 'Alt-f',
        '\x1bg': 'Alt-g',
        '\x1bh': 'Alt-h',
        '\x1bi': 'Alt-i',
        '\x1bj': 'Alt-j',
        '\x1bk': 'Alt-k',
        '\x1bl': 'Alt-l',
        '\x1bm': 'Alt-m',
        '\x1bn': 'Alt-n',
        '\x1bo': 'Alt-o',
        '\x1bp': 'Alt-p',
        '\x1bq': 'Alt-q',
        '\x1br': 'Alt-r',
        '\x1bs': 'Alt-s',
        '\x1bt': 'Alt-t',
        '\x1bu': 'Alt-u',
        '\x1bv': 'Alt-v',
        '\x1bw': 'Alt-w',
        '\x1bx': 'Alt-x',
        '\x1by': 'Alt-y',
        '\x1bz': 'Alt-z',
        '\x1bA': 'Shift-Alt-A',
        '\x1bB': 'Shift-Alt-B',
        '\x1bC': 'Shift-Alt-C',
        '\x1bD': 'Shift-Alt-D',
        '\x1bE': 'Shift-Alt-E',
        '\x1bF': 'Shift-Alt-F',
        '\x1bG': 'Shift-Alt-G',
        '\x1bH': 'Shift-Alt-H',
        '\x1bI': 'Shift-Alt-I',
        '\x1bJ': 'Shift-Alt-J',
        '\x1bK': 'Shift-Alt-K',
        '\x1bL': 'Shift-Alt-L',
        '\x1bM': 'Shift-Alt-M',
        '\x1bN': 'Shift-Alt-N',
        '\x1bO': 'Shift-Alt-O',
        '\x1bP': 'Shift-Alt-P',
        '\x1bQ': 'Shift-Alt-Q',
        '\x1bR': 'Shift-Alt-R',
        '\x1bS': 'Shift-Alt-S',
        '\x1bT': 'Shift-Alt-T',
        '\x1bU': 'Shift-Alt-U',
        '\x1bV': 'Shift-Alt-V',
        '\x1bW': 'Shift-Alt-W',
        '\x1bX': 'Shift-Alt-X',
        '\x1bY': 'Shift-Alt-Y',
        '\x1bZ': 'Shift-Alt-Z',
        '\x1b0': 'Alt-0',
        '\x1b1': 'Alt-1',
        '\x1b2': 'Alt-2',
        '\x1b3': 'Alt-3',
        '\x1b4': 'Alt-4',
        '\x1b5': 'Alt-5',
        '\x1b6': 'Alt-6',
        '\x1b7': 'Alt-7',
        '\x1b8': 'Alt-8',
        '\x1b9': 'Alt-9',
    }        
        
    if key in escKeys:
        return escKeys[key]
    else:
        if key.startswith('\x1b'):
            return 'ERR'
        elif len(key) == 1:
            return key
        else:
            return ''

def GetKey():

    # from: https://stackoverflow.com/questions/71801157/detect-key-press-in-python-without-running-as-root-and-without-blockingioerror
    fd = sys.stdin

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)

    newattr[3] = newattr[3] & ~termios.ICANON 
    newattr[3] = newattr[3] & ~termios.ECHO
    newattr[6][termios.VMIN] = 0
    newattr[6][termios.VTIME] = 0
    termios.tcsetattr(fd, termios.TCSANOW, newattr)


    key = ''
    try:
        while True:
            try:
                c = sys.stdin.read(1)
                if c:
                    key += c
                else:
                    return KeyToFunction(key)
            except:
                return ''
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, oldterm)


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

def PrintLines(text, offset = 0, cnt = 0):
    # Print a string, line for line, with a given offset
    cnt2 = 0
    for line in text.splitlines():
        cnt2 += 1
        CursorRight(offset)
        print(line)
        if cnt == cnt2:
            break

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
