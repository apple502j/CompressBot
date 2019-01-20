import datetime
import os
from time import sleep,time
import requests
import mw_api_client as mw

dt=datetime.datetime
tdl=datetime.timedelta

COMPRESSED=[]

def pngquanty(fobj):
    proc = os.system('pngquant --quality=50-70 --skip-if-larger --speed 5 -o "compressed.png" -f -- before.png'
                            )


def get_tsp():
    return dt.now().isoformat()

def get_file_uploads(wiki, ts):
    global COMPRESSED
    rcs=list(wiki.logevents(limit=50, lestart=ts, leend=get_tsp(), ledir="newer",
                                lenamespace="6", letype="upload"
                                ))
    rcs=list(filter(lambda rc:rc.user not in [],rcs))
    rcs=list(filter(lambda rc:rc.title.lower().endswith(".png"),rcs))
    rcs=list(filter(lambda rc:rc.title not in COMPRESSED, rcs))
    
    return rcs



w=mw.Wiki("wiki","Compress (Bot)")
w.login() # login
tsp=(dt.now()-tdl(days=1)).isoformat()


while True:
    rcs=get_file_uploads(w, tsp)
    for rc in rcs:
        
        try:
            u=w.request(action="query",prop="imageinfo",titles=rc.title,iiprop="url")
        except:
            continue
        uu=list(u["query"]["pages"].values())[0]["imageinfo"][0]["url"]
        png=requests.get(uu).content
        with open("before.png".format(time()),"w+b") as k:
            k.write(png)
        pngquanty(k)
        with open("compressed.png","rb") as k:
            try:
                w.upload(k, rc.title, "ファイルを圧縮",True)
            except:
                continue
        COMPRESSED.append(rc.title)
        sleep(5)
    tsp=(dt.now()-tdl(days=1)).isoformat()
    sleep(60)
    
