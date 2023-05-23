import threading
import requests
import cfscrape
import uuid
import random
import string

def randomstr(n):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

roomId = input("roomId: ")
nickname = input("nickname(%rand%): ")
url = requests.get("https://garticphone.com/api/server?code="+roomId).text
print(url)

def joinbot():
    while True:
        try:
            t = randomstr(7);
            s = requests.session()
            port = random.randint(10000,10049)
            proxy = "socks5://127.0.0.1:"+str(port)
            proxies = {"http":proxy,"https":proxy}
            s.proxies = proxies
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

for _ in range(100):
    threading.Thread(target=joinbot).start()
