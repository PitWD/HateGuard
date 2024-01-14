import os
import sys
import tty
import time

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
    if os.name == 'posix':  # Linux/Mac
        import select
        import termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setcbreak(sys.stdin.fileno())
            ready, _, _ = select.select([sys.stdin], [], [], 0)
            if ready:
                size = sys.stdin.__sizeof__()
                return sys.stdin.read(size)
            else:
                return ''
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    elif os.name == 'nt':  # Windows
        import msvcrt

        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8')
        else:
            return ''

    else:
        raise NotImplementedError("Unsupported operating system")

def GetKey2():
    if os.name == 'posix':  # Linux/Mac
        import select
        import termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setcbreak(fd)
            key = ''
            while True:
                ready, _, _ = select.select([fd], [], [], 0)
                if ready:
                    key += sys.stdin.read(1)
                else:
                    return KeyToFunction(key)
            # return key if key else None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    elif os.name == 'nt':  # Windows
        import msvcrt

        key = ''
        while msvcrt.kbhit():
            key += msvcrt.getch().decode('utf-8')
        # return key if key else None

    else:
        raise NotImplementedError("Unsupported operating system")


def GetKey3():
    import os
    import sys, termios, fcntl      # GetKey

    # from: https://stackoverflow.com/questions/71801157/detect-key-press-in-python-without-running-as-root-and-without-blockingioerror
    fd = sys.stdin

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)

    newattr[3] = newattr[3] & ~termios.ICANON 
    newattr[3] = newattr[3] & ~termios.ECHO
    newattr[6][termios.VMIN] = 0
    newattr[6][termios.VTIME] = 0
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    #fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)


    key = ''
    try:
        while True:
            try:
                c = sys.stdin.read(1)
                if c:
                    key += c
                    print(key)
                    #time.sleep(0.01)
                else:
                    return KeyToFunction(key)
                    #print(key)
                
            except:
                return ''
    finally:
        #termios.tcflush(fd, termios.TCIFLUSH)
        #termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        termios.tcsetattr(fd, termios.TCSANOW, oldterm)
        #fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

    #return KeyToFunction(key)


if __name__ == "__main__":
    while True:
        
        user_input = GetKey2()
        
        if user_input != '':
            print(f"You pressed: {user_input}")
            if user_input.lower() == 'q':
                break
        time.sleep(0.05)

    print("Exiting...")
