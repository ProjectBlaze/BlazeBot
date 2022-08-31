import requests
from datetime import date
base_url = "https://api.telegram.org/bot{BOTAPIHERE}/" # Used To Control Bot Via Telegram Bot API
def sendPost(codeName): # Used To Generate Rom Post
    today = date.today() # Fetches Date From System
    buildDate = today.strftime("%b-%d-%Y") # Modifies Date In Required Format
    res = requests.get("{Get Your Official device.json and Paste Link Here}").json() # Check ProjectBlaze device.json for reference
    banner = open("images/pic.png", "rb") # Opens Banner Image
    parameters = {
        "chat_id" : "{CHATID}",  # Use getUpdates to obtain chat_id of group
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
        '''.format(res["BlazeVersion"],res[codeName]["DeviceName"],codeName,buildDate,res[codeName]["UserName"],res[codeName]["DeviceChangelogs"],res[codeName]["Screenshots"],res[codeName]["Support Group"],codeName),
        "parse_mode" : "html" # Treats Caption as a HTML File
    }
    files = {
        "photo" : banner
    }
    resp = requests.get(base_url+"sendPhoto",data=parameters, files=files) # sendPhoto allow sending images
def device_check(offset): # Check If Device Is Official & Updates Message ID
    parameters = {
        "offset" : offset
    }
    official_devices = ["surya","onclite","sweet","davinci","santoni"] # Add Your Official Devices Here
    resp = requests.get(base_url+"getUpdates", data = parameters) # getUpdates fetches updates from URL
    data = resp.json() # Converts resp to json
    for i in data["result"]: # Basic Loops To Iterate And Check For Official Devices
        for j in official_devices:
            try:
                if i["message"]["text"] == "/release "+j:
                    sendPost(i["message"]["text"][9::]) # Returns Only codeName and slice '/release'
            except KeyError: # Prevent Sudden Crash Of Program Due To Key Error In Case Of No 'text' Field
                continue
    try:
        if data["result"]: # Updates Offset
            return data["result"][-1]["update_id"] + 1
    except KeyError:
        offset = data["result"][-1]["update_id"] + 1
offset = 0
while True:
    offset = device_check(offset) 
