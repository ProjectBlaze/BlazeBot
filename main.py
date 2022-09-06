import secrets
import requests
import updateOffset
import fetchData
import checkMessage
from datetime import date
chat_id = secrets.database()[1]
bot_token = secrets.database()[0]
def sendPost(codeName):
    today = date.today() # Fetches Date From System
    buildDate = today.strftime("%b-%d-%Y") # Modifies Date In Required Format
    res = requests.get("https://raw.githubusercontent.com/ProjectBlaze/official_devices/12.1/post/device.json").json()
    banner = open("images/pic.png", "rb") # Opens Banner Image
    parameters = {
        "chat_id" : "{}".format(chat_id),  # Use getUpdates to obtain chat_id of group
        "caption" : '''<b>Project Blaze v{} - OFFICIAL | Android 12L
📲 : {} ({})
📅 : {}
🧑‍💼 : @{} </b>

▪️ Changelog: <a href="https://github.com/ProjectBlaze/official_devices/blob/12.1/changelog.md">Source</a> | <a href="{}">Device</a>
▪️ <a href="https://www.projectblaze.live/download.html">Download</a>
▪️ <a href="{}">Screenshots</a>
▪️ <a href="{}">Support Group</a>
▪️ <a href="https://t.me/projectblaze">Community Chat</a>
▪️ <a href="https://t.me/projectblazeupdates">Updates Channel</a>

#Blaze #{} #Android12L #S
        '''.format("1.1",res[codeName]["DeviceName"],codeName,buildDate,res[codeName]["UserName"],res[codeName]["DeviceChangelogs"],res[codeName]["Screenshots"],res[codeName]["Support Group"],codeName),
        "parse_mode" : "html"
    }
    files = {
        "photo" : banner
    }
    requests.get("https://api.telegram.org/bot{}/sendPhoto".format(bot_token),data=parameters, files=files)
def main():
    offset = updateOffset.initialOffset(0)
    official_devices = fetchData.fetchOfficialDevices([])
    latest_message = fetchData.getLatestMessages(offset)
    messageBool = checkMessage.checkMessage(latest_message,official_devices)
    offset2 = offset
    if messageBool:
        if latest_message == "/release " + messageBool : 
            sendPost(messageBool)
            offset2 += 1
    while True:
        offset = updateOffset.initialOffset(0)
        if offset==offset2:
            main()
main()