#Mix By HF
#Multi-Process

from os import system, getcwd, chdir, path, makedirs
from glob import glob
import json
import shutil
import subprocess
import sys
from time import sleep
from datetime import datetime
if sys.platform.startswith("win"):
    import winreg
special_chars=r'\/:*?"><=|'
a=datetime.now().strftime("%Y-%m-%d %H%M%S")
# a=str(datetime.now().date())+f"_{datetime.now().hour}-{datetime.now().minute}-{datetime.now().second}"

def DownloadsPath():
    if sys.platform.startswith("win"):
        try:
            return winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"),"{374DE290-123F-4565-9164-39C4925E467B}")[0]
        except Exception:
            pass
    return path.join(path.expanduser("~"),"Downloads")

downpath = path.join(DownloadsPath(),a)
LOG=path.join(getcwd(),"Log_"+a+".txt")
WARN=path.join(getcwd(),"Warn_"+a+".txt")
ERROR=path.join(getcwd(),"Error_"+a+".txt")
TT={1:"Info",2:"Waring",3:"Error"}

def Log(typer,chars):
    chars=str(chars)
    a=str(datetime.now().date())+f"_{datetime.now().hour}-{datetime.now().minute}-{datetime.now().second}"
    b=True
    c=TT[typer]+f"[{a}]"+": "+chars+"\n"
    for t in range(5):
        try:
            with open(LOG,"a",encoding="utf-8") as f:
                f.write(c)
            if typer>=2:
                with open(WARN,"a",encoding="utf-8") as f:
                    f.write(c)
                if typer==3:
                    with open(ERROR,"a",encoding="utf-8") as f:
                        f.write(c)
            b=False
            break
        except:
            sleep(1)
    if b:
        raise BaseException

def WorkList():
    Path=path.join(getcwd(),"**","video.m4s")
    prelit=glob(Path,recursive=True)
    lit=[]
    for i in prelit:
        lit.append(i)
    return lit

def Dos(Dir):
    chdir(path.dirname(Dir))#去掉‘video.m4s’

    with open(path.join("..","entry.json"),"r",encoding="utf-8") as f:
        rdata=json.load(f)
        bvid=str(rdata["bvid"])
        try:
            title1=str(rdata['title'])
            title2=str(rdata['page_data']['download_subtitle'])
            if title2==title1+' '+title1:
                title=title1
                Log(1,f"Titled [{title}] with Method1 at {Dir}")
            else:
                title21=" P"+str(rdata['page_data']['page'])
                title22=title2.replace(title1,"")
                title20=title2.replace(title22,"")
                title=title20+title21+title22
                Log(1,f"Titled [{title}] with Method2 at {Dir}")
        except:
            title=str(rdata.get("title"))
            Log(1,f"Titled [{title}] with Method3 at {Dir}")
        finally:
            if len(title)<len(str(rdata.get("title"))):
                Log(2,f"Changed title from [{title}] to [{str(rdata.get('title'))}] at {Dir}")
                title=str(rdata.get("title"))
    #system(f"rename mixed.mkv {title}.mkv")
    title1=title

    for char in special_chars:
        title = title.replace(char," ")

    if len(title1)!=len(title):
        Log(1,f"Deleted Special Characters from [{title1}] to [{title}] at {Dir}")

    command=[
        "ffmpeg","-y",
        "-i","audio.m4s",
        "-i","video.m4s",
        "-map","0:a:0",
        "-map","1:v:0",
        "-c","copy",
        "-metadata",f"title={bvid} {title}",
        "-metadata:s:a:0","language=und",
        "-metadata:s:v:0","language=und",
        "Mixed.mkv"
    ]
    print(command)
    result=subprocess.run(command,capture_output=True,text=True)
    if result.returncode!=0:
        raise Exception("ffmpeg: "+result.stderr.strip()[-1000:])

    f=path.join(downpath,title+".mkv")
    print(f'Move Mixed.mkv to "{f}"')
    shutil.move("Mixed.mkv",f)

Wlist=WorkList()
Log(1,Wlist)
if(not path.exists(downpath)):
    makedirs(downpath)
for i in Wlist:
    try:
        Dos(i)
    except Exception as EX:
        Log(3,i+" -- "+str(EX))
if sys.platform.startswith("win"):
    system("pause")
else:
    input("Press Enter to continue...")

'''
这里使用ffmpeg进行混合, 需要ffmpeg已经加入环境变量PATH
用replace方法替换掉文件名中不能出现的特殊字符
Windows用winreg调取downloads文件夹位置, {374DE290-123F-4565-9164-39C4925E467B}代表下载文件夹目录
macOS/Linux使用~/Downloads
上一级文件夹的json文件包含视频名称
shutil.move可以在移动的同时重命名
os.chdir(path)函数用于更改当前工作目录到指定的目录
os.getcwd()函数用来遍历文件

975604735
└─c_411035633
    │  danmaku.xml
    │  entry.json
    │  
    └─116
            audio.m4s
            index.json
            video.m4s
'''
