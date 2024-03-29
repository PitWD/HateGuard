import os
import sys
import ESC
import csv
import json
import time
import MEN

ESC.CLS()

folder = ""
userID = ""
commentID = ""
commentType = ""
commentRemark = ""
commentLink = ""
firstName = ""
lastName = ""
nickName = ""
rating = ""
ratingCnt = 0
ratingOK = 0
ratingWarning = 0
ratingCritical = 0
email = ""
location = ""
website = ""
company = ""
occupation = ""
userLink = ""
comment = ""
show_links = False
remark = ""

def PrintUser():
    # Print Header
    ESC.CLS()
    ESC.ResetForeGround()
    ESC.CursorRight(2)
    MEN.PrintRainbow("H a t e G u a r d - Post/Person Of Interest")
    print(" on ("+ folder + ")\n")
    # Print User
    MEN.PrintInfoPos(' firstName', firstName)
    ESC.CursorUp(1)
    MEN.PrintInfoPos('nickName', nickName, None, ESC.Solarized16.Base0, 40)
    MEN.PrintInfoPos('  lastName', lastName)
    ESC.CursorUp(1)
    MEN.PrintInfoPos('  userID', userID, None, ESC.Solarized16.Base0, 40)
    MEN.PrintInfoPos('     eMail', email)
    ESC.CursorUp(1)
    MEN.PrintInfoPos('  rating', '', None, None, 40, "")
    MEN.PrintRating(int(rating))
    print("")
    MEN.PrintInfoPos('  location', location)
    ESC.CursorUp(1)
    MEN.PrintInfoPos(' company', company, None, None, 40)
    MEN.PrintInfoPos('   website', website)
    MEN.PrintInfoPos('occupation', '',None, None, None, "\n")
    occuTxt = ESC.BreakLines(occupation, 60)
    ESC.SetForeGround(ESC.Solarized16.Base1)
    ESC.CursorUp(1)
    ESC.PrintLines(occuTxt, 16)
    MEN.PrintInfoPos('    Remark', remark, MEN.GetRatingColor(rating), ESC.Solarized16.Base2)

    MEN.PrintInfoPos('  ratingOK', ratingOK, None, ESC.Solarized16.Green)
    ESC.CursorUp(1)
    MEN.PrintInfoPos('warning', ratingWarning, None, ESC.Solarized16.Orange, 24)
    ESC.CursorUp(1)
    MEN.PrintInfoPos('critical', ratingCritical, None, ESC.Solarized16.Red, 41)
    ESC.CursorUp(1)
    MEN.PrintInfoPos('unrated', ratingCnt, None, ESC.Solarized16.Base01, 59)


    if show_links:
        MEN.PrintInfoPos('  userLink', userLink, None, ESC.Solarized16.Base0)
    ESC.ResetForeGround()
    print("")

def PrintMenu():
    print("")
    MEN.PrintMenuPos('  o  ', "User OK", ESC.Solarized16.Green)
    ESC.CursorUp(1) 
    MEN.PrintMenuPos('w', "User WARNING", ESC.Solarized16.Yellow , None, 32)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('c', "User CRITICAL", ESC.Solarized16.Red, None, 55)
    MEN.PrintMenuPos(' del ', "Remove from POI")
    ESC.CursorUp(1) 
    MEN.PrintMenuPos('u', "Edit User", None, None, 32)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('r', "Edit Remark", None, None, 55)
    MEN.PrintMenuPos('space', "Next POI")
    ESC.CursorUp(1)
    MEN.PrintMenuPos('s', "Show Links", None, None, 32)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('q', "QUIT processing", None, None, 55)
    MEN.PrintMenuPos(' back', "Previous POI")

    print("\n    ", end="")
    print("Press Key to select an option... > ", end="")
    ESC.SetForeGround(ESC.Solarized16.Orange)
    print(" ", end="", flush=True)  
    ESC.CursorLeft(1)

def PrintComment():
    MEN.PrintInfoPos('commentID', commentID,None,None,2)
    commentTxt = ESC.BreakLines(comment, 76) 
    ESC.SetForeGround(ESC.Solarized16.Base2) 
    ESC.PrintLines(commentTxt, 2)
    if show_links:
        MEN.PrintInfoPos('link', commentLink, None, ESC.Solarized16.Base0,2)
    ESC.ResetForeGround()
    print("")

def PrintRemark():
    MEN.PrintInfoPos('    Remark', '',MEN.GetRatingColor(commentReason),None,None,"")
    ESC.TxtBold(True)
    ESC.CursorSave()
    print(commentRemark)
    ESC.TxtBold(False)
    print("")


# Get command line arguments
argCount = len(sys.argv)
for i in range(1, argCount):
    arg = sys.argv[i]
    if arg == "-f" or arg == "--folder":
        if i+1 < argCount:
            folder = sys.argv[i+1]
            print("Folder: " + folder)
            if os.path.exists(folder):
                os.chdir(folder)
            else:
                print("Folder '" + folder + "' does not exist!")
                time.sleep(3)
                sys.exit(1)
        else:
            print("Missing argument for '" + arg + "'!")
            time.sleep(3)
            sys.exit(1)

# Open poi.csv and iterate through all lines
with open('poi.csv', 'r') as f:
    reader = csv.reader(f)
    pois = list(reader)

poiID = 0
while poiID < len(pois):
    poi = pois[poiID]
    #for poi in pois:
    userID = poi[0]
    if userID != "idUser":
        commentID = poi[1]
        commentReason = poi[2]
        commentRemark = poi[3]
        
        # get comment from comments.csv
        with open('comments.csv', 'r') as f:
            reader = csv.reader(f)
            comments = list(reader)
        for comment in comments:
            if comment[0] == commentID:
                commentLink = comment[5]
                break
        
        # get user from user.csv
        with open('users.csv', 'r') as f:
            reader = csv.reader(f)
            users = list(reader)
        for user in users:
            if user[0] == userID:
                firstName = user[1]
                lastName = user[2]
                nickName = user[3]
                rating = user[4]
                email = user[5]
                location = user[6]
                website = user[7]
                company = user[8]
                occupation = user[9]
                userLink = user[10]
                remark = user[11]
                ratingCnt = 0
                ratingOK = 0
                ratingWarning = 0
                ratingCritical = 0
                # get rating from comments.csv
                with open('comments.csv', 'r') as f:
                    reader = csv.reader(f)
                    comments2 = list(reader)
                for comment2 in comments2:
                    if comment2[2] == user[0]:
                        ratingCnt += 1
                        if comment2[1] == "1":
                            ratingOK += 1
                        elif comment2[1] == "2":
                            ratingWarning += 1
                        elif comment2[1] == "3":
                            ratingCritical += 1
                break

        # get comment from comment/
        with open('comments/' + commentID + '.txt', 'r') as f:
            comment = f.read()

        pressedKey = ""
        show_links = False
        while pressedKey == "":

            os.system('stty -echo')

            PrintUser()
            # Print Comment
            PrintComment()
            # Print Remark
            PrintRemark()
            # Print Menu
            PrintMenu()

            while pressedKey != "q":
                pressedKey = ESC.GetKey()
                saveUser = 0
                savePOI = 0

                if pressedKey == "o":
                    rating = 1
                    saveUser = 1
                elif pressedKey == "w":
                    rating = 2
                    saveUser = 1
                elif pressedKey == "c":
                    rating = 3
                    saveUser = 1
                elif pressedKey == "Del":
                    # Remove line from list
                    pois.remove(poi)
                    savePOI = 1
                    pressedKey = " "
                    poiID -= 1
                elif pressedKey == "Back":
                    # Previous POI
                    poiID -= 2
                    pressedKey = " "
                    #break
                elif pressedKey == "u":
                    # Edit User
                    os.chdir('..')
                    os.system('python3 UserCLI.py -f ' + folder + ' -u ' + userID)
                    os.chdir(folder)
                    pressedKey = ""
                    break
                elif pressedKey == "r":
                    # Edit Remark
                    ESC.CursorRestore()
                    commentRemark = ESC.edlin(commentRemark)
                    poi[3] = commentRemark
                    savePOI = 1
                    pressedKey = ""
                elif pressedKey == "s":
                    # Show Links
                    show_links = not show_links
                    pressedKey = ""
                    break
                elif pressedKey == " ":
                    # Next POI
                    pass

                if saveUser == 1:
                    # Save user to users.csv
                    user[4] = rating
                    with open('users.csv', 'w') as f:
                        writer = csv.writer(f)
                        writer.writerows(users)
                    pressedKey = ""     # redraw
                    break
                if savePOI == 1:
                    # Save POI to poi.csv
                    with open('poi.csv', 'w') as f:
                        writer = csv.writer(f)
                        writer.writerows(pois)
                    if pressedKey == "":
                        break   # redraw (from edit remark)


                if pressedKey == " ":
                    # Quit menu
                    break

                time.sleep(0.1)

        os.system('stty echo')
        if pressedKey == "q":
            # Quit processing
            os.chdir('..')
            break

    poiID += 1
    if poiID >= len(pois):
        poiID = 1
    elif poiID <= 0:
        poiID = len(pois) - 1

