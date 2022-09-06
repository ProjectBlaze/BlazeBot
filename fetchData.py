import requests
import secrets
bot_token = secrets.database()[0]
def fetchOfficialDevices(list):
    data = requests.get("https://raw.githubusercontent.com/ProjectBlaze/official_devices/12.1/post/device.json").json()
    for i in data:
        list.append(i)
    return list
def getLatestMessages(offset):
    parameters = {
        "offset" : offset
    }
    data = requests.get("https://api.telegram.org/bot{}/getUpdates".format(bot_token), data = parameters).json()
    
    return data["result"][0]["message"]["text"]

