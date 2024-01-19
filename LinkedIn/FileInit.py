
import os
import json
import csv
import getpass

# Create secret.json, if missing
if not os.path.exists('secret.json'):
    data = {
        "username": "your_username",
        "password": "your_password",
        "appID": "your_clientID",
        "appSecret": "your_clientSecret",
        "redirectURL": "your_redirectURL",
        "accessToken": "your_accessToken",
    }
    with open('secret.json', 'w') as f:
        json.dump(data, f)

# Create settings.json, if missing
if not os.path.exists('settings.json'):
    data = {
        "user2scrap": "user2scrap",
        "urn2scrap": "urn2scrap",
        "autoOK": "10",
    }
    with open('settings.json', 'w') as f:
        json.dump(data, f)

# Create user.csv, if missing
if not os.path.exists('users.csv'):
    with open('users.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'firstName', 'lastName', 'nickName','rating', 'email', 'location', 'www', 'company', 'occupation', 'link', 'remark'])

# Create debug folder, if missing
if not os.path.exists('debug'):
    os.mkdir('debug')

# Create user folder, if missing
if not os.path.exists('users'):
    os.mkdir('users')

# Create posts.csv, if missing
if not os.path.exists('posts.csv'):
    with open('posts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'date', 'link','likes','shares','comments'])

# Create posts folder, if missing
if not os.path.exists('posts'):
    os.mkdir('posts')

# Create comments.csv, if missing
if not os.path.exists('comments.csv'):
    with open('comments.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'rating' 'userID', 'parentID', 'date', 'link'])

# Create comments folder, if missing
if not os.path.exists('comments'):
    os.mkdir('comments')

# Create poi.csv, if missing (Posts of Interest)
if not os.path.exists('poi.csv'):
    with open('poi.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['idUser', 'idPost', 'reason','remark'])
    
# Check, if secret.json contains individual username and password
with open('secret.json', 'r') as f:
    data = json.load(f)
    username = data['username']
    password = data['password']
    appID = data['appID']
    appSecret = data['appSecret']
    redirectURL = data['redirectURL']
    accessToken = data['accessToken']

    if username == 'your_username' or password == 'your_password':
        # No credits - Get username and password from user
        username = input('Please enter your username: ')
        password = getpass.getpass('Please enter your password: ')
        appID = input('Please enter your appID: ')
        appSecret = getpass.getpass('Please enter your appSecret: ')
        redirectURL = input('Please enter your redirectURL: ')
        accessToken = getpass.getpass('Please enter your accessToken: ')
        save_creds = input('Do you wanna save your credits (y/n): ')
        if save_creds.lower() == 'y':
            # Save credentials         
            data['username'] = username
            data['password'] = password
            data['appID'] = appID
            data['appSecret'] = appSecret
            data['redirectURL'] = redirectURL
            data['accessToken'] = accessToken
            with open('secret.json', 'w') as f:
                json.dump(data, f)

# Check, if settings.json contains individual user2scrap
with open('settings.json', 'r') as f:
    data = json.load(f)
    user2scrap = data['user2scrap']
    if user2scrap == 'user2scrap':
        # No link - Get link from user
        user2scrap = input('Please enter the user you want to scrap: ')
        urn2scrap = input('Please enter the urn you want to scrap: ')
        save_creds = input('Do you wanna save your credits (y/n): ')
        if save_creds.lower() == 'y':
            # Save credentials         
            data['user2scrap'] = user2scrap
            data['urn2scrap'] = urn2scrap
            with open('settings.json', 'w') as f:
                json.dump(data, f)
