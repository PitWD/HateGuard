import os
import sys
import tty

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
                return sys.stdin.read(1)
            else:
                return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    elif os.name == 'nt':  # Windows
        import msvcrt

        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8')
        else:
            return None

    else:
        raise NotImplementedError("Unsupported operating system")

if __name__ == "__main__":
    while True:
        user_input = GetKey()
        
        if user_input is not None:
            print(f"You pressed: {user_input}")
            if user_input.lower() == 'q':
                break

    print("Exiting...")
