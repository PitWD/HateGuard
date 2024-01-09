import sys
import ESC
import time
import MEN
import os

sys.path.append('..')

HateGuardVersion = "0.1.0a"
HateGuardDate = "10.01.2023"

def PrintMainMenu():
    ESC.CLS()

    ESC.TxtBold(True)
    ESC.SetForeGround(ESC.Solarized16.Red)
    print( "  H a ", end="")
    ESC.SetForeGround(ESC.Solarized16.Orange)
    print( "t e ", end="")
    ESC.SetForeGround(ESC.Solarized16.Yellow)
    print( "G u ", end="")
    ESC.SetForeGround(ESC.Solarized16.Green)
    print( "a r ", end="")
    ESC.SetForeGround(ESC.Solarized16.Cyan)
    print( "d - ", end="")
    ESC.SetForeGround(ESC.Solarized16.Blue)
    print( "CL", end="")
    ESC.SetForeGround(ESC.Solarized16.Violet)
    print( "I", end="")

    ESC.TxtBold(False)
    ESC.SetForeGround(ESC.Solarized16.Base2)
    print( " v" + HateGuardVersion, end="")
    print( " (" + HateGuardDate + ") ", end="")
    ESC.SetForeGround(ESC.Solarized16.Base01)
    print( "by github.com/PitWD/HateGuard")
    ESC.ResetForeGround()
    print( "\n")

    MEN.PrintMenuPos('h', "Show Help Screen")
    ESC.CursorUp(1)
    MEN.PrintMenuPos('q', "Quit",None, None, 40)
    print("")

    MEN.PrintMenuPos('l', "Do LinkedIn Rating")
    ESC.CursorUp(1)
    MEN.PrintMenuPos('L', "Do LinkedIn Scraping",None, None, 40)

    MEN.PrintMenuPos('t', "Do Xitter Rating", ESC.Solarized16.Base01, ESC.Solarized16.Base01)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('T', "Do Xitter Scraping",ESC.Solarized16.Base01,ESC.Solarized16.Base01, 40)

    MEN.PrintMenuPos('f', "Do Facebook Rating", ESC.Solarized16.Base01, ESC.Solarized16.Base01)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('F', "Do Facebook Scraping",ESC.Solarized16.Base01,ESC.Solarized16.Base01, 40)

    MEN.PrintMenuPos('i', "Do Instagram Rating", ESC.Solarized16.Base01, ESC.Solarized16.Base01)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('I', "Do Instagram Scraping",ESC.Solarized16.Base01,ESC.Solarized16.Base01, 40)

    print("\n    ", end="")
    print("Press Key to select an option... > ", end="")
    ESC.SetForeGround(ESC.Solarized16.Orange)
    print(" ", end="", flush=True)  
    ESC.CursorLeft(1)

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

    # wait 0.1 seconds
    time.sleep(0.1)
    if pressedKey == " ":
        # We did something, so we need to refresh the screen
        PrintMainMenu()
    elif pressedKey != "" and pressedKey != "q":
        ESC.FixEcho()
ESC.ResetForeGround()
print("\n\n")


