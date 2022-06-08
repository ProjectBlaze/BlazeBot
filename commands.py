import telegram
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler
from tqdm.contrib.telegram import tqdm, trange
from base64 import decodebytes
from database import *
from pathlib import Path
from utils.download import *
import pathlib 
import logging
import pysftp
import gdown
import time
import math
import gdown
import requests
import paramiko
import os
import shutil
import json
import datetime
import pytz


# Some Global Variables
HOME = os.path.expanduser("~") 
with open(f'{HOME}/secrets.txt', 'r') as file:
    content = file.read().replace('\n', ',')
    content = content.split(',')
    token = content[0]
    sfpass = content[1]
    CHAT_ID = content[2]

# Host key for pysftp
keydata = b"""AAAAC3NzaC1lZDI1NTE5AAAAIOQD35Ujalhh+JJkPvMckDlhu4dS7WH6NsOJ15iGCJLC"""
key = paramiko.Ed25519Key(data=decodebytes(keydata))
cnopts = pysftp.CnOpts()
cnopts.hostkeys.add('frs.sourceforge.net', 'ssh-ed25519', key)

# Official device list
devurl = "https://raw.githubusercontent.com/ProjectBlaze/vendor_blaze/12.1/blaze.devices"
gdevurl = "https://github.com/ProjectBlaze/vendor_blaze/blob/12.1/blaze.devices"
req = requests.get(devurl)
if req.status_code in [200]:
    devices = req.text
else:
    print(f"Could not retrieve: {devurl}, err: {req.text} - status code: {req.status_code}")
devices = devices.replace('\n', ',')
devices = devices.split(',')

# Start Command
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if str(update.effective_chat.id) not in CHAT_ID :
        await context.bot.send_message(update.effective_chat.id, text="Commands aren't supported here")
        return
    mess_id = update.effective_message.message_id
    mess = '''
Hello, I am BlazeBot.
Use /help to know how to use me.
'''

    await context.bot.send_message(CHAT_ID, reply_to_message_id=mess_id, text=mess)

# Help Command
async def help(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if str(update.effective_chat.id) not in CHAT_ID :
        await context.bot.send_message(update.effective_chat.id, text="Commands aren't supported here")
        return
    mess_id = update.effective_message.message_id
    mess = '''
Helping guide for using me:

Supported commands :
1. /start
2. /help
3. /post

You can use any command without any arguments for help related to that command.

'''
    await context.bot.send_message(CHAT_ID, reply_to_message_id=mess_id, text=mess)

# Post command
async def post(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if str(update.effective_chat.id) not in CHAT_ID :
        await context.bot.send_message(update.effective_chat.id, text="Commands aren't supported here")
        return
    mess_id = update.effective_message.message_id
    help = f'''
Use this command in following format to make post for your device.

/post device_codename device_changelog_link

device_codename is codename for your device.
Please use UpperCase letters if you did same <a href="{gdevurl}">here</a>

device_changelog_link is telegraph link of changelog for your device.

e.g. :
/post onclite https://telegra.ph/Changelogs-11-05-08
'''
    dmess = f'''
Sorry, I couldn't find your device codename <a href="{gdevurl}" >here</a>.
Please make PR if you didn't.
'''
    arg = context.args
    codename = None
    dclog = None
    try:
        codename = arg[0]
        dclog = arg[1]
    except IndexError:
        await context.bot.send_message(CHAT_ID, reply_to_message_id=mess_id, text=help, parse_mode='HTML', disable_web_page_preview=True)
        return
    if codename in devices:
        pass
    else:
        await content.bot.send_message(CHAT_ID, reply_to_message_id=mess_id, text=dmess, parse_mode='HTML', disable_web_page_preview=True)
        return
    if dclog == None:
        pass
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    day = current_time.day
    month = current_time.month
    month = months[month]
    year = current_time.year
    date = f" {month}-{day}-{year} "
    mess = f'''
Project Blaze v{database['BlazeVersion']} - OFFICIAL | Android 12L
📲 : {database[codename]['device']} ({codename})
📅 : {date}
🧑‍💼 : {database[codename]['maintainer']}

▪️ Changelog: <a href="https://github.com/ProjectBlaze/official_devices/blob/12.1/changelog.md" >Source</a> | <a href="{dclog}" >Device</a>
▪️ <a href="https://www.projectblaze.live/download.html" >Download</a>
▪️ <a href="https://t.me/projectblazeupdates/97" >Screenshots</a>
▪️ <a href="{database[codename]['sgroup']}" >Support Group</a>
▪️ <a href="https://t.me/projectblaze" >Community Chat</a>
▪️ <a href="https://t.me/projectblazeupdates" >Updates Channel</a>

#Blaze #{codename} #Android12L #S
'''
    await context.bot.send_photo(CHAT_ID, photo=open('images/blaze1.2.png', 'rb'), caption=mess, reply_to_message_id=mess_id, parse_mode='HTML')

# Upload command
async def upload(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if str(update.effective_chat.id) not in CHAT_ID :
        await context.bot.send_message(update.effective_chat.id, text="Commands aren't supported here")
        return
    mess_id = update.effective_message.message_id
    # SourceForge variables
    username = "ganesh314159"
    chat_id = update.effective_chat.id
    # if confirmChat(chat_id):
    #     chat_id = chat_id
    # else:
    #     mess = "Sorry, my master didn't allowed me to message in this chat"
    #     await context.bot.send_message(chat_id, reply_to_message_id=mess_id, text=mess)
    #     return
    bmess_id = mess_id+1
    arg = context.args
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
    dmess = f'''
Sorry, I couldn't find your device codename <a href="{gdevurl}" >here</a>.
Please make PR if you didn't.
'''
    urlmess = f'''
Please provide GDrive url.
Use /upload for more info.
'''
    try:
        codename = arg[0]
        try:
            gdurl = arg[1]
        except IndexError:
            await context.bot.send_message(CHAT_ID, reply_to_message_id=mess_id, text=urlmess)
            return
    except IndexError:
        await context.bot.send_message(CHAT_ID, reply_to_message_id=mess_id, text=help, parse_mode='HTML', disable_web_page_preview=True)
        return
    if codename in devices:
        pass
    else:
        await context.bot.send_message(CHAT_ID, reply_to_message_id=mess_id, text=dmess, parse_mode='HTML', disable_web_page_preview=True)
        return
    name = get_file_details(gdurl)['name']
    size = get_file_details(gdurl)['size']
    mess = f'''
File : 🗂️ <a href="{gdurl}" >{name}</a> 🗂️
Status : Downloading...📤
Size : {size}
Target : 🌐 GoogleDrive 🌐
'''
    await context.bot.send_message(CHAT_ID, reply_to_message_id=mess_id, text=mess, parse_mode='HTML', disable_web_page_preview=True)
    file_path = gdown.download(url=gdurl, output='temp/')
    target_url = f'https://sourceforge.net/projects/projectblaze/files/{codename}/'
    mess2 = f'''
File : 🗂️ <a href="{gdurl}" >{name}</a> 🗂️
Status : Uploading...📤
Size : {size}
Target : 🌐 <a href="{target_url}">projectblaze/{codename}</a> 🌐
'''
    await context.bot.edit_message_text(chat_id=chat_id, message_id=mess_id, text=mess2, parse_mode='HTML', disable_web_page_preview=True)
    with pysftp.Connection('frs.sourceforge.net', username='ganesh314159', password=sfpass, cnopts=cnopts) as sftp:
        with sftp.cd(f'/home/frs/project/projectblaze/{codename}'):
            sftp.put(f'{file_path}')
    mess3 = f'''
File : 🗂️ <a href="{gdurl}" >{name}</a> 🗂️
Status : Uploaded✅
Target : 🌐 <a href="{target_url}">projectblaze/{codename}</a> 🌐
'''
    os.remove(f'temp/{name}')
    await context.bot.edit_message_text(chat_id=chat_id, message_id=mess_id, text=mess3, parse_mode='HTML', disable_web_page_preview=True)


async def test(update: Update, context: CallbackContext.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    print(f"Type of chat_id is '{chat_id}'.")
    print(f"Type of CHAT_ID is '{CHAT_ID}'.")
    if str(update.effective_chat.id) not in CHAT_ID :
        await context.bot.send_message(chat_id, text="Commands aren't supported here")
        return
    chat_id = update.effective_chat.id
    mess_id = update.effective_message.message_id
    user = update.effective_user.username
    await context.bot.send_message(CHAT_ID, reply_to_message_id=mess_id, text="Message from supported group")




