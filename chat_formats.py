def start_message():
    start = '''
Hello, I am BlazeBot.
Use /help to know how to use me.
'''
    return start

def help_message():
    help = '''
Helping guide for using me:

Supported commands :
1. /start
2. /help
3. /post

You can use any command without any arguments for help related to that command.

'''
    return help

def post_help_message(gdevurl):
    help_message = f'''
Use this command in following format to make post for your device.

/post device_codename

device_codename is codename for your device.
Please use UpperCase letters if you did same <a href="{gdevurl}">here</a>

e.g. :
/post onclite
'''

def codename_failed_message(gdevurl):
    failed_message = f'''
Sorry, I couldn't find your device codename <a href="{gdevurl}" >here</a>.
Please make PR if you didn't.
'''
    return failed_message

def post_changelog_message(codename):
    changelog = f'''
Please make device changelog file for {codename} <a href="https://github.com/ProjectBlaze/official_devices/tree/14/device">here.</a>
'''
    return changelog

def post_message(codename, database, date, dclog):
    post = f'''
#Blaze #{codename} #Android14 #U #Stable
<strong>Project Blaze v{database['BlazeVersion']} - OFFICIAL | Android 14 | QPR3
📲 : {database[codename]['device']} ({codename})
📅 : {date}
🧑‍💼 : {database[codename]['maintainer']}

▪️ Changelog:</strong> <a href="https://github.com/ProjectBlaze/official_devices/blob/14/changelog.md" >Source</a> | <a href="{dclog}" >Device</a>
▪️ <a href="https://www.projectblaze.in/" >Download</a>
▪️ <a href="https://t.me/projectblaze/123678" >Screenshots</a>
▪️ <a href="{database[codename]['sgroup']}" >Support Group</a>
▪️ <a href="https://t.me/projectblaze" >Community Chat</a>
▪️ <a href="https://t.me/projectblazeupdates" >Updates Channel</a>
'''
    return post

def upload_help_message(gdevurl):
    help = f'''
Use this command in following format to upload GDrive files to SourceForge.

/upload device_codename gdrive_link

device_codename is codename for your device.
Please use UpperCase letters if you did same <a href="{gdevurl}">here</a>

gdrive_link is GoogleDrive link of Blaze rom file for your device.

Make sure your GDrive file is public.
e.g. :
/upload onclite https://drive.google.com/uc?id=1UZ_HrwsCDA6yobGSrHgbLgn_Vvud_s3G&export=download

Note :- 
1. Do not play with this command. Only use this command when you are 100% sure with your build and you want to release it.
2. Currently only GDrive links are supported. Support for other links will be added soon.
'''
    return help

def url_message():
    urlmess = f'''
Please provide GDrive url.
Use /upload for more info.
'''
    return urlmess

def file_status_message(gdurl, name, size, status, target):
    if status == 0:
        status = "Downloading...📤"
    elif status == 1:
        status = "Uploading...📤"
    elif status == 2:
        status = "Uploaded✅"
    
    if target == 0:
        target = "Source Forge"
    elif target == 1:
        target = "Google Drive"

    status_message = f'''
File : 🗂️ <a href="{gdurl}">{name}</a> 🗂️
Status : {status}
Size : {size}
Target : 🌐 {target} 🌐
'''
    return status_message
