import sys
import ESC
import time
import MEN
import os

sys.path.append('..')

HateGuardVersion = "0.1.4a"
HateGuardDate = "21.01.2023"

def PrintMainMenu():
    ESC.CLS()

    ESC.TxtBold(True)
    ESC.CursorRight(2)
    MEN.PrintRainbow("H a t e G u a r d - C L I")

    ESC.TxtBold(False)
    ESC.SetForeGround(ESC.Solarized16.Base2)
    print( " v" + HateGuardVersion, end="")
    print( " (" + HateGuardDate + ") ", end="")
    ESC.SetForeGround(ESC.Solarized16.Base01)
    print( "by github.com/PitWD/HateGuard")
    ESC.ResetForeGround()
    print( "\n")

    MEN.PrintMenuPos('h', "Show Help Screen",None, None, 6)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('q', "Quit",None, None, 42)
    print("")

    MEN.PrintMenuPos('l', "Do LinkedIn Rating",None, None, 6)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('L', "Do LinkedIn Scraping",None, None, 42)

    MEN.PrintMenuPos('t', "Do Xitter Rating", ESC.Solarized16.Base01, ESC.Solarized16.Base01,6)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('T', "Do Xitter Scraping",ESC.Solarized16.Base01, ESC.Solarized16.Base01, 42)

    MEN.PrintMenuPos('f', "Do Facebook Rating", ESC.Solarized16.Base01, ESC.Solarized16.Base01,6)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('F', "Do Facebook Scraping",ESC.Solarized16.Base01, ESC.Solarized16.Base01, 42)

    MEN.PrintMenuPos('i', "Do Instagram Rating", ESC.Solarized16.Base01, ESC.Solarized16.Base01,6)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('I', "Do Instagram Scraping",ESC.Solarized16.Base01, ESC.Solarized16.Base01, 42)

    print("")

    MEN.PrintMenuPos('p/P', "LinkedIn POI/User View",None, None)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('x/X', "Xitter POI/User View", ESC.Solarized16.Base01, ESC.Solarized16.Base01, 40)
    
    MEN.PrintMenuPos('b/B', "Facebook POI/User View", ESC.Solarized16.Base01, ESC.Solarized16.Base01)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('g/G', "Instagram POI/User View", ESC.Solarized16.Base01, ESC.Solarized16.Base01, 40)

    print("\n    ", end="")
    print("Press Key to select an option... > ", end="")
    ESC.SetForeGround(ESC.Solarized16.Orange)
    print(" ", end="", flush=True)  
    ESC.CursorLeft(1)

os.system('stty -echo')
PrintMainMenu()
pressedKey = ""
while pressedKey != "q":
    pressedKey = ESC.GetKey()
    if pressedKey == "h":
        # Print Help-File
        pass
    elif pressedKey == "l":
        # Do LinkedIn Rating
        os.system('python3 RatingCLI.py -f LinkedIn')
        pressedKey = " "
    elif pressedKey == "L":
        # Do LinkedIn Scraping
        os.chdir('LinkedIn')  
        os.system('python3 GetPostsLinkedIn.py')
        os.chdir('..')
        pressedKey = " "
    elif pressedKey == "t":
        # Do Xitter Rating
        pass
    elif pressedKey == "T":
        # Do Xitter Scraping
        pass
    elif pressedKey == "f":
        # Do Facebook Rating
        pass
    elif pressedKey == "F":
        # Do Facebook Scraping
        pass
    elif pressedKey == "i":
        # Do Instagram Rating
        pass
    elif pressedKey == "I":
        # Do Instagram Scraping
        pass
    elif pressedKey == " ":
        pressedKey = ""
    elif pressedKey == "p":
        # Do LinkedIn POI View
        os.system('python3 PoiCLI.py -f LinkedIn')
        pressedKey = " "
    elif pressedKey == "x":
        # Do Xitter POI View
        pass
    elif pressedKey == "b":
        # Do Facebook POI View
        pass
    elif pressedKey == "g":
        # Do Instagram POI View
        pass
    elif pressedKey == "P":
        # Do LinkedIn POI View
        os.system('python3 UserCLI.py -f LinkedIn')
        pressedKey = " "
    elif pressedKey == "X":
        # Do Xitter POI View
        pass
    elif pressedKey == "B":
        # Do Facebook POI View
        pass
    elif pressedKey == "G":
        # Do Instagram POI View
        pass

    # wait 0.1 seconds
    time.sleep(0.05)
    if pressedKey == " ":
        # We did something, so we need to refresh the screen
        PrintMainMenu()
        # We may need to reset the echo
        os.system('stty -echo')

ESC.ResetForeGround()
print("\n\n")
os.system('stty echo')


