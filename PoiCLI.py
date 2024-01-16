import os
import sys
import ESC
import csv
import json
import time
import MEN

ESC.CLS()
os.system('stty -echo')

folder = ""
userID = ""
commentID = ""
commentType = ""
commentRemark = ""
firstName = ""
lastName = ""
nickName = ""
rating = ""
email = ""
location = ""
website = ""
company = ""
occupation = ""
comment = ""

def PrintUser():
    # Print Header
    ESC.CLS()
    ESC.ResetForeGround()
    ESC.CursorRight(2)
    MEN.PrintRainbow("H a t e G u a r d - Post/Person Of Interest")
    print(" on ("+ folder + ") while comment: ", end="")
    ESC.SetForeGround(ESC.Solarized16.Base2)
    print(commentID)
    print("")
    ESC.ResetForeGround()
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
    MEN.PrintInfoPos(' location', location)
    ESC.CursorUp(1)
    MEN.PrintInfoPos('company', company, None, None, 40)
    MEN.PrintInfoPos('   website', website)
    MEN.PrintInfoPos('occupation', '',None, None, None, "")
    occuTxt = ESC.BreakLines(occupation, 60)
    ESC.SetForeGround(ESC.Solarized16.Base1)
    ESC.PrintLines(occuTxt, 13)
    ESC.ResetForeGround()
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

for poi in pois:
    if poi[0] == "id":
        continue
    userID = poi[0]
    commentID = poi[1]
    commentReason = poi[2]
    commentRemark = poi[3]

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

    # get comment from comment/
    with open('comments/' + commentID + '.txt', 'r') as f:
        comment = f.read()

    PrintUser()
    # Print Comment
    comment = ESC.BreakLines(comment, 76) 
    ESC.SetForeGround(ESC.Solarized16.Base2) 
    ESC.PrintLines(comment, 2) 
    ESC.ResetForeGround()
    print("")
    # Print Remark
    MEN.PrintInfoPos('    Remark', commentRemark,MEN.GetRatingColor(commentType),None,None,"")
    ESC.TxtBold(True)
    print(commentRemark)
    ESC.TxtBold(False)
    print("")

                    
