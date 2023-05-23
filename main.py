import threading
import requests
import uuid
import random
import string
import time
import base64
import os
import json
import hashlib
import html
try:import discord
except:os.system("pip3 install discord");import discord

client = discord.Client(intents=discord.Intents.all())

def randomstr(n):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

key = os.environ['key']
global urls
urls = {}
global roomIds
roomIds = []
global nicknames
nicknames = ["ニックネーム%rand%"]

myname = os.getcwd().split("/")[-1]

with open('code.py', 'rb') as file:
    fileData = file.read()
    version = hashlib.md5(fileData).hexdigest()
print(version)
sha = None
try:sha = requests.get("https://api.github.com/repos/ghub09331/ghub/contents/repls/"+myname,headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer "+key}).json()["sha"]
except:pass
requests.put("https://api.github.com/repos/ghub09331/ghub/contents/repls/"+myname,headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer "+key},json={"message":version+" update","committer":{"name":"ghub09331","email":"ghub09331@gmail.com"},"content":base64.b64encode(version.encode()).decode()}).json()

@client.event
async def on_ready():
    global urls
    global roomIds
    global nicknames
    channel = await client.fetch_channel("1110505904601837602")
    messages = [message async for message in channel.history(limit=1)]
    try:
        config = json.loads(messages[0].content)
        roomIds = config["roomIds"]
        nicknames = config["nicknames"]
        print(config)
        turls = {}
        for roomId in roomIds:
            turls[roomId] = requests.get("https://garticphone.com/api/server?code="+roomId).text
        urls = turls
    except:pass
    

@client.event
async def on_message(message):
    global urls
    global roomIds
    global nicknames
    try:
        config = json.loads(message.content)
        roomIds = config["roomIds"]
        nicknames = config["nicknames"]
        print(config)
        turls = {}
        for roomId in roomIds:
            turls[roomId] = requests.get("https://garticphone.com/api/server?code="+roomId).text
        urls = turls
    except:pass
    

def updater():
    global urls
    global roomIds
    global nicknames
    while True:
        try:
            config = json.loads(html.unescape(requests.get("https://www.youtube.com/watch?v=Zgkn2MR5A5w").text.split('<meta name="description" content="')[1].split('"')[0]))
            roomIds = config["roomIds"]
            nicknames = config["nicknames"]
            print(config)
            turls = {}
            for roomId in roomIds:
                turls[roomId] = requests.get("https://garticphone.com/api/server?code="+roomId).text
            urls = turls
        except:pass
        time.sleep(1)

def joinbot():
    while True:
        if roomIds == []:time.sleep(5);continue
        try:
            roomId = random.choice(roomIds)
            url = urls[roomId]
            nickname = random.choice(nicknames)
            t = randomstr(7);
            s = requests.session()
            sid = s.get(url+"/socket.io/?EIO=3&transport=polling&t="+t).text.split('{"sid":"')[1].split('"')[0]
            uuid_ = str(uuid.uuid4())
            skin = str(random.randint(0,45))
            nick = nickname.replace("%rand%",str(random.randint(1,9999)))
            body = str('[1,"'+uuid_+'","'+nick+'",'+skin+',"ja",false,"'+roomId+'",null,null]')
            body = str(str(len(body)+2)+":42"+body).encode("utf-8")
            res = s.post(url+"/socket.io/?EIO=3&transport=polling&t="+t+"&sid="+sid, headers={"Content-Type":"text/plain;charset=UTF-8"}, data=body).text
        except:pass
#        except Exception as e:print(e)

#threading.Thread(target=updater).start()
for _ in range(10):
    threading.Thread(target=joinbot).start()

client.run(os.environ['token'])
