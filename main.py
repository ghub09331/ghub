import threading
import requests
import uuid
import random
import string
import time
import base64

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

def updater():
    global url
    global nickname
    while True:
        try:
            roomId = base64.b64decode(requests.get("https://api.github.com/repos/ghub09331/ghub/contents/room.id",headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer "+key}).json()["content"].encode()).decode()
            url = requests.get("https://garticphone.com/api/server?code="+roomId).text
        except:pass

def joinbot():
    while True:
        if url == "":time.sleep(5);continue
        try:
            t = randomstr(7);
            s = requests.session()
            sid = s.get(url+"/socket.io/?EIO=3&transport=polling&t="+t).text.split('{"sid":"')[1].split('"')[0]
            print(sid)
            uuid_ = str(uuid.uuid4())
            print(uuid_)
            skin = str(random.randint(0,45))
            nick = nickname.replace("%rand%",str(random.randint(100,9999)))
            body = str('[1,"'+uuid_+'","'+nick+'",'+skin+',"ja",false,"'+roomId+'",null,null]')
            body = str(str(len(body)+2)+":42"+body).encode("utf-8")
            print(body)
            res = s.post(url+"/socket.io/?EIO=3&transport=polling&t="+t+"&sid="+sid, headers={"Content-Type":"text/plain;charset=UTF-8"}, data=body).text
            print(res)
        except:pass
#        except Exception as e:print(e)

for _ in range(10):
    threading.Thread(target=joinbot).start()
