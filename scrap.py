import json
import os
import shutil
import requests as r

import subprocess

def confirmation():
    f1=os.listdir()
    for i in f1:
        while i=="temp":
            shutil.rmtree("temp")
            break
        while i =="buildtemp":
            shutil.rmtree("buildtemp")
        while i =="Build":
            f2=open("hashlist.json")
            f3=json.load(f2)
            f4=len(f3)
            f5=os.listdir("build/json")
            f6=len(f5)
            while f4!=f6:
                shutil.rmtree("build")
                break
            while f4==f6:
                print("Build Folder Already Exist... ")
                print("Do You Wants To Continue However.")
                f7=input('"Y" For YES,"N" for NO .....')
                if f7=="Y":
                    shutil.rmtree("Build")
                break
            break

        
        break

    print("All Done Check the build folder")
   
def snapshoturi():
    #1
    l = []
    f1 = open("hashlist.json", "r+")
    f2 = json.load(f1)
    f3 = len(f2)
    l1 = os.listdir()
    os.mkdir("buildtemp")
    os.mkdir("temp")
    f5 = subprocess.run(
        "metaboss decode mint -L hashlist.json -o temp -t 120 ")
    f6 = os.listdir("temp")
    for i in f6:
        f7 = open("temp/"+i, "r+")
        f8 = json.load(f7)
        f9 = f8["uri"]
        l.append(f9)
    f10 = open("urilinks.json", "w+")
    json.dump(l, f10)
    print("done!!!!!!!!")



    
def scrapdata():
    #2

    m1 = open("urilinks.json", "r+")
    m2 = json.load(m1)
    m3 = len(m2)
    for i in range(0, m3):

        url = m2[i]
        f1 = r.get(url)
        f2 = json.loads(f1.content)

        f3 = open(""+"buildtemp/"+str(i)+".json", "w+")
        f5 = json.dump(f2, f3, sort_keys=True)


def image():
    #3
    os.mkdir("Build")
    os.mkdir("Build/json")
    os.mkdir("Build/png")
    m1 = open("urilinks.json", "r+")
    m2 = json.load(m1)
    m3 = len(m2)
    for i in range(0, m3):
        f1 = open(""+"buildtemp/"+str(i)+".json", "r+")
        f2 = json.load(f1)
        f3 = f2["image"]

        res = r.get(f3, stream=True)

        if res.status_code == 200:
            with open(""+"buildtemp/"+str(i)+".png", 'wb') as f:
                shutil.copyfileobj(res.raw, f)

        print(str(m3-(i+1))+" remaining")


def dropbuild():
    #4
    f2 = open("urilinks.json", "r+")
    f3 = json.load(f2)
    f4 = len(f3)
    for j in range(0, f4):
        f5=open(""+"buildtemp/"+str(j)+".json","r+")
        f6=json.load(f5)
        f7=f6["name"]
        f8=f7.split("#")[-1]
        f5.close()
        os.rename(""+"buildtemp/"+str(j)+".json",""+"build/json/"+f8+".json")
        os.rename(""+"buildtemp/"+str(j)+".png",""+"build/png/"+f8+".png")
    shutil.rmtree("buildtemp")
    shutil.rmtree("temp")
        


confirmation()
snapshoturi()
scrapdata()
image()
dropbuild()

