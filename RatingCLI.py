import os
import sys
import ESC
import csv
import json
import time
import MEN

ESC.CLS()

folder = ""

def PrintRating(rating):
    if rating == 1:
        ESC.SetForeGround(ESC.Solarized16.Green)
        print("OK", end="")
    elif rating == 2:
        ESC.SetForeGround(ESC.Solarized16.Orange)
        print("WARNING", end="")
    elif rating == 3:
        ESC.SetForeGround(ESC.Solarized16.Red)
        print("CRITICAL", end="")
    else:
        ESC.SetForeGround(ESC.Solarized16.Blue)
        print("UNKNOWN", end="")

def PrintMenu():
    print("")
    MEN.PrintMenuPos('  o  ', "User OK")
    MEN.PrintMenuPos('w', "User WARNING", None, None, 40)
    MEN.PrintMenuPos('  c  ', "User CRITICAL")
    MEN.PrintMenuPos('q', "QUIT processing",None, None, 40)
    MEN.PrintMenuPos('space', "Comment OK", ESC.Solarized16.Green)
    MEN.PrintMenuPos('-', "Comment WARNING", ESC.Solarized16.Yellow, None, 40)
    MEN.PrintMenuPos('enter', "Comment CRITICAL", ESC.Solarized16.Red)
    print("\n    ", end="")
    print("Press Key to select an option... > ", end="")
    ESC.SetForeGround(ESC.Solarized16.Orange)
    print(" ", end="", flush=True)  
    ESC.CursorLeft(1)

# Get command line arguments
argCount = len(sys.argv)
for i in range(1, argCount):
    arg = sys.argv[i]
    if arg == "-f" or arg == "--folder":
        if i+1 < argCount:
            folder = sys.argv[i+1]
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

# Open comments.csv and iterate backwards through all comments
with open('comments.csv', 'r') as f:
    reader = csv.reader(f)
    comments = list(reader)
    comments.reverse()

    for comment in comments:
        postFile = ""
        commentFile = ""
        parentFile = ""
        commentDate = comment[4]
        # Check, if comment is unrated
        if comment[1] == "0" or comment[1] == 0:
            # Open comment file
            with open('comments/comment_' + comment[0] + '.txt', 'r') as f:
                commentFile = f.read()
            
            # Find user of comment
            with open('users.csv', 'r') as f:
                reader = csv.reader(f)
                users = list(reader)
                users.reverse()
                for user in users:
                    if user[0] == comment[2]:
                        userName = user[1] + " " + user[2]
                        userRating = int(user[4])
                        userCompany = user[8]
                        userOccupation = user[9]
                        break
            
            # Check if parent is a post
            with open('posts.csv', 'r') as f:
                reader = csv.reader(f)
                posts = list(reader)
                posts.reverse()
                for post in posts:
                    if post[0] == comment[3]:
                        # Open post file
                        with open('posts/post_' + post[0] + '.txt', 'r') as f:
                            postFile = f.read()
                        break
            
            # Check if parent is a comment
            if postFile == "":
                with open('comments.csv', 'r') as f:
                    reader = csv.reader(f)
                    comments2 = list(reader)
                    comments2.reverse()
                    for comment2 in comments2:
                        if comment2[0] == comment[3]:
                            # Open parent file
                            with open('comments/comment_' + comment2[0] + '.txt', 'r') as f:
                                parentFile = f.read()
                            break
                try:
                    # Open parent - post
                    with open('posts/post_' + comment2[3] + '.txt', 'r') as f:
                        postFile = f.read()
                except:
                    # Parent is a comment, too
                    with open('comments/comment_' + comment2[3] + '.txt', 'r') as f:
                        postFile = f.read()

            # Print Post History
            ESC.CLS()
            if postFile != "":
                ESC.SetForeGround(ESC.Solarized16.Base01)
                postFile = ESC.BreakLines(postFile, 60)
                ESC.PrintLines(postFile, 19, 5)

            if parentFile != "":
                ESC.SetForeGround(ESC.Solarized16.Base0)
                parentFile = ESC.BreakLines(parentFile, 60)
                ESC.PrintLines(parentFile, 10, 7)

            # Print User Infos
            ESC.SetForeGround(ESC.Solarized16.Base1)
            ESC.TxtBold(1)
            ESC.CursorRight(2)
            print(userName, end="")
            ESC.TxtBold(0)
            print(" (", end="")
            PrintRating(userRating) 
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
            # Print Comment
            ESC.SetForeGround(ESC.Solarized16.Base2)
            commentFile = ESC.BreakLines(commentFile, 60)
            ESC.PrintLines(commentFile, 2)
            ESC.ResetForeGround()

            # Print Menu
            PrintMenu()

            # Get Key
            pressedKey = ""
            saveUser = 0
            saveComment = 0
            while pressedKey != "q":
                pressedKey = ESC.GetKey()
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
                elif pressedKey == "enter":
                    # Comment CRITICAL
                    comment[1] = 3
                    saveComment = 1
                    

                        





                        # Update comments.csv
                        with open('comments.csv', 'w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerows(comments)

                        # Print comment
                        ESC.ResetForeGround()
                        print("\n\n")
                        print("Post: " + postFile)
                        ESC.ResetForeGround()
                        print("Comment: " + commentFile)
                        print("Rating: ", end="")
                        ESC.SetForeGround(ESC.Solarized16.Orange)
                        print(rating, end="", flush=True)  
                        ESC.CursorLeft(1)

                        # Wait 0.5 seconds
                        time.sleep(0.5)

                        # Update comments.csv
                        with open('comments.csv', 'w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerows(comments)

                        # Print comment
                        ESC.ResetForeGround()
                        print("\n\n")
                        print("Post: " + postFile)
                        ESC.ResetForeGround()
                        print("Comment: " + commentFile)
                        print("Rating: ", end="")
                        ESC.SetForeGround(ESC.Solarized16.Orange)
                        print(rating, end="", flush=True)  
                        ESC.CursorLeft(1)
                
                
                            
                # Update comments.csv
                with open('comments.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(comments)

                # Print comment
                ESC.ResetForeGround()
                print("\n\n")
                print("Comment: " + comment[5])
                print("Rating: ", end="")
                ESC.SetForeGround(ESC.Solarized16.Orange)
                print(comment[1], end="", flush=True)  
                ESC.CursorLeft(1)

                # Wait 0.5 seconds
                time.sleep(0.5)