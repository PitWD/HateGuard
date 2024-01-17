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
remark = ""
'''
commentID = ""
commentType = ""
commentRemark = ""
commentLink = ""
'''
firstName = ""
lastName = ""
nickName = ""
rating = ""
email = ""
location = ""
website = ""
company = ""
occupation = ""
userLink = ""
comment = ""
commentList = []
show_links = False
commentCnt = 0
ratingOK = 0
ratingWarning = 0
ratingCritical = 0

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
    MEN.PrintInfoPos('    Remark', remark, MEN.GetRatingColor(rating))

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
    MEN.PrintMenuPos('  1  ', "Edit 1st Name")
    ESC.CursorUp(1) 
    MEN.PrintMenuPos('2', "Last Name", None, None, 32)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('e', "eMail", None, None, 55)
    MEN.PrintMenuPos('  l  ', "Edit Location")
    ESC.CursorUp(1) 
    MEN.PrintMenuPos('t', "Web-Site", None, None, 32)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('y', "Company", None, None, 55)
    MEN.PrintMenuPos('  p  ', "PrintLastComment")
    ESC.CursorUp(1) 
    MEN.PrintMenuPos('P', "10 Comments", None, None, 32)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('A', "All Comments", None, None, 55)
    MEN.PrintMenuPos('space', "Next User")
    ESC.CursorUp(1) 
    MEN.PrintMenuPos('f', "Find User", None, None, 32)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('s', "Show Links", None, None, 55)
    MEN.PrintMenuPos(' back', "Previous User")
    ESC.CursorUp(1)
    MEN.PrintMenuPos('r', "Edit Remark", None, None, 32)
    ESC.CursorUp(1)
    MEN.PrintMenuPos('q', "QUIT processing", None, None, 55)

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
with open('users.csv', 'r') as f:
    reader = csv.reader(f)
    users = list(reader)

userPos = 0
while userPos < len(users):
    user = users[userPos]
    userID = user[0]
    ratingOK = 0
    ratingWarning = 0
    ratingCritical = 0
    commentCnt = 0

    if userID != "id":
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

        # make list of all comments of this user
        with open('comments.csv', 'r') as f:
            reader = csv.reader(f)
            comments = list(reader)
        commentList = []
        for comment in comments:
            if comment[2] == userID:
                if comment[1] == "1":
                    ratingOK += 1
                elif comment[1] == "2":
                    ratingWarning += 1
                elif comment[1] == "3":
                    ratingCritical += 1
                commentList.append(comment)

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

                if pressedKey == "o":
                    rating = 1
                    saveUser = 1
                elif pressedKey == "w":
                    rating = 2
                    saveUser = 1
                elif pressedKey == "c":
                    rating = 3
                    saveUser = 1
                elif pressedKey == "1":
                    # Edit 1st Name
                    print("")
                    user[1] = ESC.edlin(firstName)
                    saveUser = 1
                elif pressedKey == "2":
                    # Edit Last Name
                    print("")
                    user[2] = ESC.edlin(lastName)
                    saveUser = 1
                elif pressedKey == "e":
                    # Edit eMail
                    print("")
                    user[5] = ESC.edlin(email)
                    saveUser = 1
                elif pressedKey == "l":
                    # Edit Location
                    print("")
                    user[6] = ESC.edlin(location)
                    saveUser = 1
                elif pressedKey == "t":
                    # Edit Web-Site
                    print("")
                    user[7] = ESC.edlin(website)
                    saveUser = 1
                elif pressedKey == "y":
                    # Edit Company
                    print("")
                    user[8] = ESC.edlin(company)
                    saveUser = 1
                elif pressedKey == "p":
                    # Print Last Comment
                    commentCnt = 1
                elif pressedKey == "P":
                    # Print 10 Comments
                    commentCnt = 10 
                elif pressedKey == "A":
                    # Print All Comments
                    commentCnt = len(commentList)
                elif pressedKey == "f":
                    # Find User
                    pass
                elif pressedKey == "r":
                    # Edit Remark
                    print("")
                    user[11] = ESC.edlin(remark)
                    saveUser = 1
                    pressedKey = ""
                elif pressedKey == "s":
                    # Show Links
                    show_links = not show_links
                    pressedKey = ""
                    break
                elif pressedKey == "Back":
                    # Previous User
                    userPos -= 2
                elif pressedKey == " ":
                    # Next User
                    pass

                if saveUser == 1:
                    # Save user to users.csv
                    user[4] = rating
                    with open('users.csv', 'w') as f:
                        writer = csv.writer(f)
                        writer.writerows(users)
                    pressedKey = ""     # redraw
                    break

                if pressedKey == " ":
                    # Quit menu
                    break

                time.sleep(0.1)

        os.system('stty echo')
        if pressedKey == "q":
            # Quit processing
            os.chdir('..')
            break

    userPos += 1
    if userPos < 1:
        userPos = len(users) - 1
    elif userPos >= len(users):
        userPos = 1

