'''
We will use this file to get the posts of a user from LinkedIn
We will use the LinkedIn API to get the posts
We will store settings in json files
We will store data in csv files

'''

import os
import json
import csv
import ast
import re
import datetime
import sys
sys.path.append('..')
import ESC
import MEN

cLight = 37
cGrey = 92
cDark = 92
cRed = 31
cOrange = 91
cGreen = 32
cYellow = 33
cAqua = 36

debug_level = 2

postCnt = 0
commentCnt = 0
moreCommentCnt = 0

def print_dict(d, indent=0, color = cGreen):
    # Nice colorized print of a dict / list
    ESC.ResetForeGround()
    if isinstance(d, dict) and d:
        for key, value in d.items():
            ESC.ResetForeGround()            
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                print_dict(value, indent+1, color)
            else:
                # Check if value is encapsulated in a '[]'
                if isinstance(value, list):
                    #ESC.SetForeGround(cOrange)
                    for val in value:
                        print_dict(val, indent+1, cAqua)
                else:
                    ESC.SetForeGround(color)
                    print('\t' * (indent+1) + str(value))
    else:
        ESC.SetForeGround(cRed)
        print(d)
    ESC.ResetForeGround()

def extract_integer_and_identifier(s):
    # LinkedIn's postDate is a string like '1w • Edited •'
    match = re.match(r'^(\d+)(\D+)', s)
    if match:
        integer = int(match.group(1))
        identifier = match.group(2).strip().split(' ')[0]
        return integer, identifier
    else:
        return None, None

def get_post_date(postDate):
    integer, identifier = extract_integer_and_identifier(postDate)
    # Get current date
    now = datetime.datetime.now()
    # Calculate postDate
    if identifier == 'm':
        postDate = now - datetime.timedelta(minutes = integer)
    elif identifier == 'h':
        postDate = now - datetime.timedelta(hours = integer)
    elif identifier == 'd':
        postDate = now - datetime.timedelta(days = integer)
    elif identifier == 'w':
        postDate = now - datetime.timedelta(weeks = integer)
    elif identifier == 'mo':
        postDate = now - datetime.timedelta(months = integer)
    else: # identifier == 'y':
        postDate = now - datetime.timedelta(years = integer)
    # Convert postDate to string (DD.MM.YYYY HH:MM:SS)
    postDate = postDate.strftime("%d.%m.%Y %H:%M:%S")
    return postDate

def get_comment_timestamp(timeStamp):
    timeStamp = int(timeStamp) / 1000
    # Convert timeStamp to string (DD.MM.YYYY HH:MM:SS)
    timeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime("%d.%m.%Y %H:%M:%S")
    return timeStamp

def user_to_users(commenterID, firstName, lastName, nickName, occupation, userLink, picture):
    # Check if user.csv already contains commenterID on field 'id'
    userExist = 0
    with open('users.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == commenterID:
                # User already in user.csv
                userExist = 1
                break
    # Append user to user.csv if commenterID doesn't exist
    if not userExist:
        with open('users.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([commenterID, firstName, lastName, nickName, "0", "N/A", "N/A", "N/A", "N/A", occupation, userLink,picture])
    return userExist

def comment_to_comments(commentID, commenterID, parentID, timeStamp, permaLink, commentText):
    # Check if comments.csv already contains commentID on field 'id'
    commentExist = 0
    with open('comments.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == commentID:
                # Comment already in comments.csv
                commentExist = 1
                break
    # Append comment to comments.csv if commentID doesn't exist
    if not commentExist:
        with open('comments.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([commentID, "0", commenterID, parentID, timeStamp, permaLink])  
        with open('comments/' + commentID + '.txt', 'w', encoding='utf-8') as f:
                    f.write(commentText)  
    return commentExist

def fix_commentID(commentID):
    # Remove all leading chars including the first '('
    commentID = commentID.split('(', 1)[-1]
    # Remove all trailing chars including the first ','
    commentID = commentID.rsplit(',', 1)[0]
    return commentID


ESC.ResetBackGround()
ESC.ResetForeGround()
ESC.CLS()

#Run FileInit.py (Initialize files and folders)
os.system('python3 FileInit.py')

ESC.CLS()
ESC.CursorRight(2)
MEN.PrintRainbow("H a t e G u a r d - GetPostsLinkedIn.py")
print("\n")


# Get username and password from secret.json
with open('secret.json', 'r') as f:
    data = json.load(f)
    username = data['username']
    password = data['password']

# Get user2scrap from settings.json
with open('settings.json', 'r') as f:
    data = json.load(f)
    user2scrap = data['user2scrap']

print ("    Scrape Posts from LinkedIn\n")

# Import LinkedIn API
from linkedin_api import Linkedin
import linkedin_api.settings as api_dirs


# Create LinkedIn object
api = Linkedin(username, password)

cookieFile = api_dirs.COOKIE_PATH + username + '.jr'

print ("    API connected: " + str(api))
print ("    Scraping user: " + user2scrap)
print ("      Cookie file: " + cookieFile + "\n")  

#user = api.get_profile(public_id=user2scrap)
#print_dict(user)
sys.exit(1)

try:
    # Get the x most recent posts of user2scrap
    posts = api.get_profile_posts(public_id=user2scrap, post_count=10)
except:
    ESC.SetForeGround(cRed)
    print("\n\n*******************************")
    print("Error: Broken get_profile_posts")
    print("The cookie file might be broken")
    print("Cookie gets deleted............")
    # Delete cookie file
    try:
        os.remove(cookieFile)
    except:
        pass
    print("*******************************\n\n")
    ESC.ResetForeGround()
    print("\n\n")
    
    print("Retry to login and get posts...")
    try:
        api = Linkedin(username, password)
        posts = api.get_profile_posts(public_id=user2scrap, post_count=10)
    except:
        sys.exit("Error: Can't login to LinkedIn")

# Iterate over posts
for post in posts:

    postCnt += 1

    if debug_level > 0:
        # Save Post
        with open('debug/post_'+ str(postCnt)+'.json', 'w') as f:
            json.dump(post, f)   

    # Get postID, it's under updateMetadata.urn
    postID = post['updateMetadata']['urn']
    # Remove non-numeric parts in front of the postID
    postID = re.findall(r'\d+', postID)[0]

    postLink = 'https://www.linkedin.com/feed/update/urn:li:activity:' + postID + '/'

    # Get (rough) postDate, it's under actor.subDescription.text
    postDate = get_post_date(post['actor']['subDescription']['text'])  # 	1w • Edited •

    numLikes = post['socialDetail']['totalSocialActivityCounts']['numLikes']
    numShares = post['socialDetail']['totalSocialActivityCounts']['numShares']
    numComments = post['socialDetail']['totalSocialActivityCounts']['numComments']

    # Get postText, it's under commentary.text.text
    postText = post['commentary']['text']['text']

    # Check if posts.csv already contains postID on field 'id'
    postExist = 0
    lastCommentsCnt = 0
    with open('posts.csv', 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    # Update the desired row
    for row in rows:
        if row[0] == postID:
            postExist = 1
            lastCommentsCnt = row[5]
            row[3] = numLikes
            row[4] = numShares
            row[5] = numComments
            # Write the rows back to the file
            with open('posts.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            break

    # Append post to posts.csv if postID doesn't exist
    if not postExist:
        with open('posts.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([postID, postDate, postLink, numLikes, numShares, numComments])
        # Write post to posts folder
        with open('posts/' + postID + '.txt', 'w', encoding='utf-8') as f:
            f.write(postText)

    if debug_level > 0:
        print("\n\n")
        print('post_'+str(postCnt)+'.json')
        ESC.SetForeGround(cAqua)
        print(postID)
        print(postDate)    
        print(numLikes)
        print(numShares)
        print(str(numComments) + " / " + str(lastCommentsCnt))
        ESC.SetForeGround(cDark)
        print(postText + "\n\n")
    
    commentCnt = 0

    if str(numComments) != str(lastCommentsCnt):   # New comments

        comments = api.get_post_comments(postID)

        # Iterate over comments
        for comment in comments:

            commentCnt += 1

            if debug_level > 0:
                # Save comment (its a dict) in a txt file
                with open('debug/comment_'+str(postCnt)+'_'+str(commentCnt)+'.json', 'w') as f:
                    json.dump(comment, f)   

            commenterType = 'com.linkedin.voyager.feed.MemberActor'

            try:
                firstName = comment['commenter'][commenterType]['miniProfile']['firstName']
            except:
                commenterType = 'com.linkedin.voyager.feed.InfluencerActor'
            try:
                firstName = comment['commenter'][commenterType]['miniProfile']['firstName']
            except:
                if debug_level > 0:
                    ESC.SetForeGround(cRed)
                    print("\n\n****************************")
                    print("New/Unknown feed.???Actor")
                    print('comment_'+str(postCnt)+'_'+str(commentCnt)+'.json')
                    print("****************************")
                    ESC.ResetForeGround()
                    print("\n\n")
                    # Script will crash now...

            firstName = comment['commenter'][commenterType]['miniProfile']['firstName']
            lastName = comment['commenter'][commenterType]['miniProfile']['lastName']
            nickName = comment['commenter'][commenterType]['miniProfile']['publicIdentifier']
            commenterID = comment['commenter'][commenterType]['miniProfile']['objectUrn']
            
            # Remove non-numeric parts in front of the ID
            commenterID = re.findall(r'\d+', commenterID)[0]

            commentID = fix_commentID(comment['dashEntityUrn'])
            
            parentID = postID
            occupation = comment['commenter'][commenterType]['miniProfile']['occupation']
            try:
                picture = comment['commenter'][commenterType]['miniProfile']['picture']['com.linkedin.common.VectorImage']['rootUrl'] + comment['commenter']['com.linkedin.voyager.feed.MemberActor']['miniProfile']['picture']['com.linkedin.common.VectorImage']['artifacts'][0]['fileIdentifyingUrlPathSegment']
            except:
                picture = "N/A"

            timeStamp = get_comment_timestamp(comment['createdTime'])
            commentText = comment['commentV2']['text']
            permaLink = comment['permalink']

            userLink = 'https://www.linkedin.com/in/' + nickName + '/'

            if debug_level > 0:
                print("\n\n")
                print('comment_'+str(postCnt)+'_'+str(commentCnt)+'.json')
                ESC.SetForeGround(cAqua)
                print(firstName + " " + lastName + " (" + nickName + ") [" + commenterID + "]")
                print(occupation)
                print(parentID + " -> " + commentID)
                print(timeStamp)
                ESC.SetForeGround(cDark)
                print(commentText + "\n\n")

            user_to_users(commenterID, firstName, lastName, nickName, occupation, userLink, picture)
            comment_to_comments(commentID, commenterID, parentID, timeStamp, permaLink, commentText)

            # Get more comments
            moreComments = comment['socialDetail']['comments']['elements']

            moreCommentCnt = 0
           
            if str(moreComments) != '[]':  # Probably more comments
                                
                for moreComment in moreComments:    # 1st level

                    #if moreComment != 'dashEntityUrn':    # No more comments if text is '"dashEntityUrn"'
                        
                    moreCommentCnt += 1
                    
                    if debug_level > 0:
                        # Save comment (its a dict) in a txt file
                        with open('debug/moreComment_'+str(postCnt)+'_'+str(commentCnt)+'_'+str(moreCommentCnt)+'.json', 'w') as f:
                            json.dump(moreComment, f)   

                    try:

                        parentID = commentID

                        timeStamp = get_comment_timestamp(moreComment['createdTime'])
                        commentText = moreComment['commentV2']['text']
                        permaLink = moreComment['permalink']

                        commentID2 = fix_commentID(moreComment['dashEntityUrn'])
                    
                        # Extract most user-info from encapsulated dict
                        user = moreComment['commenterForDashConversion']['image']['attributes']
                        # Remove leading and trailing '[' and ']' if they exist
                        user = str(user).strip('[]')
                        # Make dict from string
                        user = ast.literal_eval(user)

                        firstName = user['miniProfile']['firstName']
                        lastName = user['miniProfile']['lastName']
                        nickName = user['miniProfile']['publicIdentifier']
                        commenterID = user['miniProfile']['objectUrn']
                        commenterID = re.findall(r'\d+', commenterID)[0]
                        occupation = user['miniProfile']['occupation']
                        try:
                            picture = user['miniProfile']['picture']['com.linkedin.common.VectorImage']['rootUrl'] + user['miniProfile']['picture']['com.linkedin.common.VectorImage']['artifacts'][0]['fileIdentifyingUrlPathSegment']
                        except:
                            picture = "N/A"

                        if debug_level > 0:
                            print('moreComment_'+str(postCnt)+'_'+str(commentCnt)+'_'+str(moreCommentCnt)+'.json')

                            ESC.SetForeGround(cAqua)
                            # print("\n\n")

                            print(firstName + " " + lastName + " (" + nickName + ") [" + commenterID + "]")
                            print(occupation)
                            print(parentID + " -> " + commentID2)
                            print(timeStamp)
                            ESC.SetForeGround(cDark)
                            print(commentText + "\n\n")

                        user_to_users(commenterID, firstName, lastName, nickName, occupation, userLink, picture)
                        comment_to_comments(commentID2, commenterID, parentID, timeStamp, permaLink, commentText)

                    except:
                        if debug_level > 0:
                            ESC.SetForeGround(cRed)
                            print("\n\n*************************")
                            print("Error: Broken moreComment")
                            print('moreComment_'+str(postCnt)+'_'+str(commentCnt)+'_'+str(moreCommentCnt)+'.json')
                            print("*************************\n\n")
                            ESC.ResetForeGround()
                            print("\n\n")
                            if debug_level > 1:
                                print_dict(moreComment)
                                print("\n\n")
                        pass

'''
            print(" cookie: ", cookie.name)
            try:
                expires = int(cookie.expires)
                expires = datetime.datetime.fromtimestamp(expires).strftime('%d.%m.%Y %H:%M:%S')
                now = datetime.datetime.fromtimestamp(int(_now)).strftime('%d.%m.%Y %H:%M:%S')
            except:
                expires = "None"
                now = "None"
            print("expires: ", expires)
            print("   _now: ", now)
            print("")
'''
        
# End of GetPostsLinkedIn.py

