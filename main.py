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

def randomstr(n):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

key = os.environ['key']
global config
config = {"url":""}
global url
url = ""
global roomId
roomId = ""
global nickname
nickname = "ニックネーム%rand%"

myname = os.getcwd().split("/")[-1]

with open('code.py', 'rb') as file:
    fileData = file.read()
    version = hashlib.md5(fileData).hexdigest()
print(version)
sha = None
try:sha = requests.get("https://api.github.com/repos/ghub09331/ghub/contents/repls/"+myname,headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer "+key}).json()["sha"]
except:pass
requests.put("https://api.github.com/repos/ghub09331/ghub/contents/repls/"+myname,headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer "+key},json={"message":version+" update","committer":{"name":"ghub09331","email":"ghub09331@gmail.com"},"content":base64.b64encode(version.encode()).decode()}).json()

def updater():
    global url
    global roomId
    global nickname
    while True:
        try:
            config = json.loads(requests.get("https://discord.com/api/guilds/1110505904601837599/widget.json?"+str(time.time)).json()["name"])
            roomId = config["roomId"]
            nickname = config["nickname"]
            print(config)
            url = requests.get("https://garticphone.com/api/server?code="+roomId).text
        except:pass
        time.sleep(2)

def joinbot():
    while True:
        if roomId == "":time.sleep(5);continue
        try:
            t = randomstr(7);
            s = requests.session()
            sid = s.get(url+"/socket.io/?EIO=3&transport=polling&t="+t).text.split('{"sid":"')[1].split('"')[0]
            uuid_ = str(uuid.uuid4())
            skin = str(random.randint(0,45))
            nick = nickname.replace("%rand%",str(random.randint(100,9999)))
            body = str('[1,"'+uuid_+'","'+nick+'",'+skin+',"ja",false,"'+roomId+'",null,null]')
            body = str(str(len(body)+2)+":42"+body).encode("utf-8")
            res = s.post(url+"/socket.io/?EIO=3&transport=polling&t="+t+"&sid="+sid, headers={"Content-Type":"text/plain;charset=UTF-8"}, data=body).text
        except:pass
#        except Exception as e:print(e)

threading.Thread(target=updater).start()
for _ in range(10):
    threading.Thread(target=joinbot).start()
