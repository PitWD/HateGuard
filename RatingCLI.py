import os
import sys
import ESC
import csv
import json
import time
import MEN

ESC.CLS()

folder = ""

def PrintMenu():
    print("")
    MEN.PrintMenuPos('  o  ', "User OK", ESC.Solarized16.Green)
    ESC.CursorUp(1) 
    MEN.PrintMenuPos('w', "User WARNING", ESC.Solarized16.Yellow , None, 32)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('c', "User CRITICAL", ESC.Solarized16.Red, None, 55)
    MEN.PrintMenuPos('space', "Comment OK", ESC.Solarized16.Green)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('i', "OK & POI", ESC.Solarized16.Green, None, 32)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('I', "OK & POI & Rem.", ESC.Solarized16.Green, None, 55)
    MEN.PrintMenuPos('  -  ', "Comment WARNING", ESC.Solarized16.Yellow)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('_', "WARNING & POI", ESC.Solarized16.Yellow, None, 32)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('/', "WARN & POI & Rem.", ESC.Solarized16.Yellow, None, 55)
    MEN.PrintMenuPos('  +  ', "Comment CRITICAL", ESC.Solarized16.Red)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('#', "CRITICAL & POI", ESC.Solarized16.Red, None, 32)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('*', "CRIT & POI & Rem.", ESC.Solarized16.Red, None, 55)

    MEN.PrintMenuPos('  F  ', "Full Text Len", ESC.Solarized16.Blue)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('q', "QUIT processing", None, None, 32)

    print("\n    ", end="")
    print("Press Key to select an option... > ", end="")
    ESC.SetForeGround(ESC.Solarized16.Orange)
    print(" ", end="", flush=True)  
    ESC.CursorLeft(1)

def PrintPrePosts(postFile, parentFile, textLen):
    #Print Header and Post History
    ESC.CLS()
    ESC.CursorRight(2)
    MEN.PrintRainbow("H a t e G u a r d - Rating-CLI")
    print(" 4 ("+ folder + ") on comment: ", end="")
    ESC.SetForeGround(ESC.Solarized16.Base2)
    print(comment[0])
    print("")
    # Print Post History
    if postFile != "":
        ESC.SetForeGround(ESC.Solarized16.Base01)
        postFile = ESC.BreakLines(postFile, 60)
        ESC.PrintLines(postFile, 19, 5)

    if parentFile != "":
        ESC.SetForeGround(ESC.Solarized16.Base0)
        parentFile = ESC.BreakLines(parentFile, 60)
        ESC.PrintLines(parentFile, 10, textLen)

def PrintUserPost(commentFile, userName, userRating, userOccupation, userCompany, commentDate):
    # Print User Infos
    ESC.SetForeGround(ESC.Solarized16.Base1)
    ESC.TxtBold(1)
    ESC.CursorRight(2)
    print(userName, end="")
    ESC.TxtBold(0)
    print(" (", end="")
    MEN.PrintRating(userRating) 
    ESC.SetForeGround(ESC.Solarized16.Base1)
    print(")")
    ESC.SetForeGround(ESC.Solarized16.Base01)
    userOccupation = ESC.BreakLines(userOccupation, 60)
    ESC.PrintLines(userOccupation, 2, 1)
    ESC.PrintLines(userCompany, 2, 1)
    ESC.TxtBold(1)
    ESC.CursorRight(2)
    print(commentDate)
    ESC.TxtBold(0)
    ESC.CursorUp(1)
    MEN.PrintInfoPos('OK', ratingOK, None, ESC.Solarized16.Green, 27)
    ESC.CursorUp(1)
    MEN.PrintInfoPos('Warn.', ratingWarning, None, ESC.Solarized16.Orange, 36)
    ESC.CursorUp(1)
    MEN.PrintInfoPos('Crit.', ratingCritical, None, ESC.Solarized16.Red, 47)
    ESC.CursorUp(1)
    MEN.PrintInfoPos('Total', ratingCnt, None, ESC.Solarized16.Base01, 58)

    # Print Comment
    ESC.SetForeGround(ESC.Solarized16.Base2)
    commentFile = ESC.BreakLines(commentFile, 60)
    ESC.PrintLines(commentFile, 2)
    ESC.ResetForeGround()


def GetRemark():
    print("\n\n")
    ESC.ResetForeGround()
    print("    Input Remark > ", end="")
    return ESC.edlin("")

def AddToPOI(user, comment, rating, remark):
    with open('poi.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user, comment, rating, remark])

folder = ""
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

# Get autoOK (Minimum Count of OK-Comments for autoOK)
with open('settings.json', 'r') as f:
    data = json.load(f)
    autoOK = int(data['autoOK'])

# Open comments.csv and iterate backwards (newest 1st) through all comments
with open('comments.csv', 'r') as f:
    reader = csv.reader(f)
    comments = list(reader)
    textLen = 7

    for comment in reversed(comments):
        postFile = ""
        commentFile = ""
        parentFile = ""
        ratingCnt = 0
        ratingOK = 0
        ratingWarning = 0
        ratingCritical = 0
        
        try:    # if int(comment[1]) fails, we are done with comments... 
            commentRating = int(comment[1])
        except:
            break

        commentDate = comment[4]

        # Check, if comment is unrated
        if not commentRating:
            # Find user of comment
            with open('users.csv', 'r') as f:
                reader = csv.reader(f)
                users = list(reader)
                for user in users:
                    if user[0] == comment[2]:
                        userName = user[1] + " " + user[2]
                        userRating = int(user[4])
                        userCompany = user[8]
                        userOccupation = user[9]
                        # Find all ratings of user
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

            # Check, if user is not rated as OK
    #        print("ratingOK: " + str(ratingOK) + " autoOK: " + str(autoOK) + " ratingWarning: " + str(ratingWarning) + " ratingCritical: " + str(ratingCritical))
            if userRating != 1 and ratingOK < autoOK or ratingWarning != 0 or ratingCritical != 0:
                # Open comment file
                with open('comments/' + comment[0] + '.txt', 'r') as f:
                    commentFile = f.read()
                            
                # Check if parent is a post
                with open('posts.csv', 'r') as f:
                    reader = csv.reader(f)
                    posts = list(reader)
                    posts.reverse()
                    for post in posts:
                        if post[0] == comment[3]:
                            # Open post file
                            with open('posts/' + post[0] + '.txt', 'r') as f:
                                postFile = f.read()
                            break
                
                # Check if parent is a comment
                if postFile == "":
                    with open('comments.csv', 'r') as f:
                        reader = csv.reader(f)
                        comments2 = list(reader)
                        for comment2 in reversed(comments2):
                            if comment2[0] == comment[3]:
                                # Open parent file
                                with open('comments/' + comment2[0] + '.txt', 'r') as f:
                                    parentFile = f.read()
                                break
                    try:
                        # Open parent - post
                        with open('posts/' + comment2[3] + '.txt', 'r') as f:
                            postFile = f.read()
                    except:
                        # Parent is a comment, too
                        with open('comments/' + comment2[3] + '.txt', 'r') as f:
                            postFile = f.read()


                pressedKey = ""
                while pressedKey == "": # For 2nd view vie menu 'F'

                    os.system('stty -echo')

                    #Print Header and Post History
                    PrintPrePosts(postFile, parentFile, textLen)
                    # Print User Infos
                    PrintUserPost(commentFile, userName, userRating, userOccupation, userCompany, commentDate)
                    # Print Menu
                    PrintMenu()

                    # Get Key
                    saveUser = 0
                    saveComment = 0
                    textLen = 7 

                    while pressedKey != "q":
                        pressedKey = ESC.GetKey()
                        saveUser = 0
                        saveComment = 0
                        remark = ""

                        # OK
                        if pressedKey == "I":
                            remark = GetRemark()
                            pressedKey = "i"
                        if pressedKey == "i":
                            AddToPOI(user[0], comment[0], 1, remark)
                            pressedKey = " "
                        
                        # WARNING
                        if pressedKey == "/":
                            remark = GetRemark()
                            pressedKey = "_"
                        if pressedKey == "_":
                            AddToPOI(user[0], comment[0], 2, remark)
                            pressedKey = "-"

                        # CRITICAL
                        if pressedKey == "*":
                            remark = GetRemark()
                            pressedKey = "#"
                        if pressedKey == "#":
                            AddToPOI(user[0], comment[0], 3, remark)
                            pressedKey = "+"

                        if pressedKey == "o":
                            # User OK
                            user[4] = 1
                            saveUser = 1
                        elif pressedKey == "w":
                            # User WARNING
                            user[4] = 2
                            saveUser = 1    
                        elif pressedKey == "c":
                            # User CRITICAL
                            user[4] = 3
                            saveUser = 1
                        elif pressedKey == " ":
                            # Comment OK
                            comment[1] = 1
                            saveComment = 1
                        elif pressedKey == "-":
                            # Comment WARNING
                            comment[1] = 2
                            saveComment = 1
                        elif pressedKey == "+":
                            # Comment CRITICAL
                            comment[1] = 3
                            saveComment = 1
                        elif pressedKey == "F":
                            # Full Text Length
                            textLen = 0
                            pressedKey = ""
                            break
                        if saveUser == 1:
                            # Update users.csv
                            with open('users.csv', 'w', newline='') as f:
                                writer = csv.writer(f)
                                writer.writerows(users)
                        elif saveComment == 1:
                            # Update comments.csv
                            with open('comments.csv', 'w', newline='') as f:
                                #commentsTmp = comments.reverse()
                                writer = csv.writer(f)
                                writer.writerows(comments)
                            pressedKey = " "
                                
                        if pressedKey == " ":
                            # Leave Menu - next comment
                            break

                        time.sleep(0.1)
                os.system('stty echo')
                if pressedKey == "q":
                    # Quit processing
                    os.chdir('..')
                    break



