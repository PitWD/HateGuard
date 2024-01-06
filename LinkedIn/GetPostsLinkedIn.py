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
import ESC
import datetime

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

def print_dict(d, indent=0):
    ESC.ResetForeGround()
    if isinstance(d, dict) and d:
        for key, value in d.items():
            ESC.ResetForeGround()            
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                print_dict(value, indent+1)
            else:
                # Check if value is encapsulated in a '[]'
                if isinstance(value, list):
                    ESC.SetForeGround(cOrange)
                else:
                    ESC.SetForeGround(cGreen)
                print('\t' * (indent+1) + str(value))
    else:
        ESC.SetForeGround(cRed)
        print(d)
    ESC.ResetForeGround()

def extract_integer_and_identifier(s):
    match = re.match(r'^(\d+)(\D+)', s)
    if match:
        integer = int(match.group(1))
        identifier = match.group(2).strip().split(' ')[0]
        return integer, identifier
    else:
        return None, None

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
            writer.writerow([commentID, commenterID, parentID, timeStamp, permaLink])  
        with open('comments/' + commentID + '.txt', 'w', encoding='utf-8') as f:
                    f.write(commentText)  
    return commentExist

def fix_commentID(commentID):
    # Remove all leading chars including the first '('
    commentID = commentID.split('(', 1)[-1]
    # Remove all trailing chars including the first ','
    commentID = commentID.rsplit(',', 1)[0]
    return commentID

#Run FileInit.py (Initialize files and folders)
os.system('python3 FileInit.py')

# Get username and password from secret.json
with open('secret.json', 'r') as f:
    data = json.load(f)
    username = data['username']
    password = data['password']

# Get user2scrap from settings.json
with open('settings.json', 'r') as f:
    data = json.load(f)
    user2scrap = data['user2scrap']

# Import LinkedIn API
from linkedin_api import Linkedin

# Create LinkedIn object
api = Linkedin(username, password)

print("\n\n")
print(api)
print(user2scrap)
print("\n\n")

# Get the x most recent posts of user2scrap
posts = api.get_profile_posts(public_id=user2scrap, post_count=5)


# Iterate over posts
for post in posts:

    postCnt += 1

    if debug_level > 0:
        # Save Post
        with open('post_'+ str(postCnt)+'.json', 'w') as f:
            json.dump(post, f)   

    # Get postID, it's under updateMetadata.urn
    postID = post['updateMetadata']['urn']
    # Remove non-numeric parts in front of the postID
    postID = re.findall(r'\d+', postID)[0]

    postLink = 'https://www.linkedin.com/feed/update/urn:li:activity:' + postID + '/'

    # Get (rough) postDate, it's under actor.subDescription.text
    # m = minutes
    # h = hours
    # d = days
    # w = weeks
    # mo = months
    # y (probably) = years (probably)
    postDate = post['actor']['subDescription']['text']  # 	1w • Edited •
    postDateVal, postDateUnit = extract_integer_and_identifier(postDate)
    print(postDateVal)
    print(postDateUnit)

    # Get current date
    now = datetime.datetime.now()
    # Calculate postDate
    if postDateUnit == 'm':
        postDate = now - datetime.timedelta(minutes = postDateVal)
    elif postDateUnit == 'h':
        postDate = now - datetime.timedelta(hours = postDateVal)
    elif postDateUnit == 'd':
        postDate = now - datetime.timedelta(days = postDateVal)
    elif postDateUnit == 'w':
        postDate = now - datetime.timedelta(weeks = postDateVal)
    elif postDateUnit == 'mo':
        postDate = now - datetime.timedelta(months = postDateVal)
    else: # postDateUnit == 'y':
        postDate = now - datetime.timedelta(years = postDateVal)
    # Convert postDate to string (DD.MM.YYYY HH:MM:SS)
    postDate = postDate.strftime("%d.%m.%Y %H:%M:%S")

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
        for row in reader:
            if row[0] == postID:
                # Post already in comments.csv
                postExist = 1
                lastCommentsCnt = row[5]
                # Update num???-variables of row in posts.csv
                row[3] = numLikes
                row[4] = numShares
                row[5] = numComments
                # Write updated row to posts.csv
                with open('posts.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(row)
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
        ESC.SetForeGround(cAqua)
        print("\n\n")
        print(postID)
        print(postDate)    
        print(numLikes)
        print(numShares)
        print(numComments)
        ESC.SetForeGround(cDark)
        print(postText + "\n\n")
    
    commentCnt = 0

    if numComments > lastCommentsCnt:   # New comments

        comments = api.get_post_comments(postID)

        # Iterate over comments
        for comment in comments:

            commentCnt += 1

            if debug_level > 0:
                # Save comment (its a dict) in a txt file
                with open('comment'+str(postCnt)+'_'+str(commentCnt)+'.json', 'w') as f:
                    json.dump(comment, f)   
                if debug_level > 1:
                    print_dict(comment)
                    print("\n\n")

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
                    print('comment'+str(postCnt)+'_'+str(commentCnt)+'.json')
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
            timeStamp = int(comment['createdTime']) / 1000
            # Convert timeStamp to string (DD.MM.YYYY HH:MM:SS)
            timeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime("%d.%m.%Y %H:%M:%S")
            commentText = comment['commentV2']['text']
            permaLink = comment['permalink']

            userLink = 'https://www.linkedin.com/in/' + nickName + '/'

            if debug_level > 0:
                ESC.SetForeGround(cAqua)
                print("\n\n")

                print(firstName + " " + lastName + " (" + nickName + ") [" + commenterID + "]")
                print(occupation)
                print(picture)
                print(parentID + " -> " + commentID)
                print(permaLink)
                print(timeStamp)
                ESC.SetForeGround(cDark)
                print(commentText + "\n\n")

            user_to_users(commenterID, firstName, lastName, nickName, occupation, userLink, picture)
            comment_to_comments(commentID, commenterID, parentID, timeStamp, permaLink, commentText)

            # Get more comments
            moreComments = comment['socialDetail']['comments']['elements']
            # Remove leading and trailing '[' and ']' if they exist
            moreComments = str(moreComments).strip('[]')
            # Make dict from string
            try:
                moreComments = ast.literal_eval(moreComments)
            except:
                if debug_level > 0:
                    ESC.SetForeGround(cRed)
                    print("\n\n****************************")
                    print("Couldn't create moreComments")
                    print('comment'+str(postCnt)+'_'+str(commentCnt)+'.json')
                    print("****************************")
                    ESC.ResetForeGround()
                    print("\n\n")
                    if debug_level > 1:
                        print_dict(moreComments)
                        print("\n\n")
                else:
                    pass
            
            moreCommentCnt = 0

            for moreComment in moreComments:    # 1st level

                moreCommentCnt += 1

                if debug_level > 0:
                    # Save comment (its a dict) in a txt file
                    with open('moreComment_'+str(postCnt)+'_'+str(commentCnt)+'_'+str(moreCommentCnt)+'.json', 'w') as f:
                        json.dump(moreComment, f)   

                try:

                    parentID = commentID
                    timeStamp = int(moreComment['createdTime']) / 1000
                    # Convert timeStamp to string (DD.MM.YYYY HH:MM:SS)
                    timeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime("%d.%m.%Y %H:%M:%S")
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
                        print("***************************************")

                        ESC.SetForeGround(cAqua)
                        # print("\n\n")

                        print(firstName + " " + lastName + " (" + nickName + ") [" + commenterID + "]")
                        print(occupation)
                        print(picture)
                        print(parentID + " -> " + commentID2)
                        print(permaLink)
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
        # Get commentID
        commentID = comment['id']

        # Get userID
        userID = comment['author']['id']

        # Get postID
        postID = post['id']

        # Get commentDate
        commentDate = comment['created_at']

        # Get commentLink
        commentLink = comment['permalink']

        # Write comment to comments.csv
        with open('comments.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([commentID, userID, postID, commentDate, commentLink])

        # Write comment to comments folder
        with open('comments/' + commentID + '.json', 'w') as f:
            json.dump(comment, f)


        # Get commentID
        commentID = comment['id']

        # Get userID
        userID = comment['author']['id']

        # Get postID
        postID = post['id']

        # Get commentDate
        commentDate = comment['created_at']

        # Get commentLink
        commentLink = comment['permalink']

        # Write comment to comments.csv
        with open('comments.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([commentID, userID, postID, commentDate, commentLink])

        # Write comment to comments folder
        with open('comments/' + commentID + '.json', 'w') as f:
            json.dump(comment, f)
'''
        

# End of GetPostsLinkedIn.py

