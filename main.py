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
import aiohttp

def randomstr(n):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


#token = os.environ['token']
#key = os.environ['key']
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
#sha = None
#try:sha = requests.get("https://api.github.com/repos/ghub09331/ghub/contents/repls/"+myname,headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer "+key}).json()["sha"]
#except:pass
#requests.put("https://api.github.com/repos/ghub09331/ghub/contents/repls/"+myname,headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer "+key},json={"message":"version data","committer":{"name":"ghub09331","email":"ghub09331@gmail.com"},"content":base64.b64encode(version.encode()).decode()}).json()

#@tasks.loop(seconds=10)
#async def update_config():
#    global urls
#    global roomIds
#    global nicknames
#    channel = await client.fetch_channel("1110505904601837602")
#    messages = [message async for message in channel.history(limit=1)]
#    try:
#        config = json.loads(messages[0].content)
#        roomIds = config["roomIds"]
#        nicknames = config["nicknames"]
#        print(config)
#        turls = {}
#        for roomId in roomIds:
#            async with aiohttp.ClientSession() as session:
#                async with session.get("https://garticphone.com/api/server?code="+roomId) as r:
#                    url = await r.text()
#            turls[roomId] = url
#        urls = turls
#    except:pass
#
#@client.event
#async def on_ready():
#    global urls
#    global roomIds
#    global nicknames
#    channel = await client.fetch_channel("1110505904601837602")
#    messages = [message async for message in channel.history(limit=1)]
#    try:
#        config = json.loads(messages[0].content)
#        roomIds = config["roomIds"]
#        nicknames = config["nicknames"]
#        print(config)
#        turls = {}
#        for roomId in roomIds:
#            async with aiohttp.ClientSession() as session:
#                async with session.get("https://garticphone.com/api/server?code="+roomId) as r:
#                    url = await r.text()
#            turls[roomId] = url
#        urls = turls
#    except:pass
#    update_config.start()
#
#@client.event
#async def on_message(message):
#    global urls
#    global roomIds
#    global nicknames
#    try:
#        config = json.loads(message.content)
#        roomIds = config["roomIds"]
#        nicknames = config["nicknames"]
#        print(config)
#        turls = {}
#        for roomId in roomIds:
#            async with aiohttp.ClientSession() as session:
#                async with session.get("https://garticphone.com/api/server?code="+roomId) as r:
#                    url = await r.text()
#            turls[roomId] = url
#        urls = turls
#    except:pass
#
#@client.event
#async def on_message_edit(bmessage,message):
#    global urls
#    global roomIds
#    global nicknames
#    try:
#        config = json.loads(message.content)
#        roomIds = config["roomIds"]
#        nicknames = config["nicknames"]
#        print(config)
#        turls = {}
#        for roomId in roomIds:
#            async with aiohttp.ClientSession() as session:
#                async with session.get("https://garticphone.com/api/server?code="+roomId) as r:
#                    url = await r.text()
#            turls[roomId] = url
#        urls = turls
#    except:pass



def updater():
    global urls
    global roomIds
    global nicknames
    while True:
        try:
            config = requests.get("https://garticcontrol.ghub09331.repl.co/?n="+myname+"&v="+version,timeout=5).json()
            roomIds = config["roomIds"]
            nicknames = config["nicknames"]
            print(config)
            turls = {}
            for roomId in roomIds:
                if roomId in urls:
                    turls[roomId] = urls[roomId]
                else:
                    turls[roomId] = requests.get("https://garticphone.com/api/server?code="+roomId,timeout=5).text
            urls = turls
        except:pass
        time.sleep(5)

def joinbot():
    while True:
        if roomIds == []:time.sleep(5);continue
        try:
            roomId = random.choice(roomIds)
            url = urls[roomId]
            nickname = random.choice(nicknames)
            t = randomstr(7);
#            s = requests.session()
            sid = requests.get(url+"/socket.io/?EIO=3&transport=polling&t="+t).text.split('{"sid":"')[1].split('"')[0]
            uuid_ = str(uuid.uuid4())
            skin = str(random.randint(0,45))
            nick = nickname.replace("%rand%",str(random.randint(1,9999)))
            body = str('[1,"'+uuid_+'","'+nick+'",'+skin+',"ja",false,"'+roomId+'",null,null]')
            body = str(str(len(body)+2)+":42"+body).encode("utf-8")
            res = requests.post(url+"/socket.io/?EIO=3&transport=polling&t="+t+"&sid="+sid, headers={"Content-Type":"text/plain;charset=UTF-8"}, data=body).text
#            print(res)
        except:pass
#        except Exception as e:print(e)

threading.Thread(target=updater).start()
for _ in range(5):
    threading.Thread(target=joinbot).start()

#client.run(os.environ['token'])
