import json
import os
import shutil
import sys
from colorama import Fore
import requests as r

jl = json.load

f1 = jl(open("eth_config.json", "r+"))
TotalSupply = f1[0]["No. Of NFTs"]
BaseUri = f1[0]["Base_Uri"]


def before():
    f1 = os.listdir()
    for i in f1:
        if i == "build":
            print("Build Folder still exsit make sure to copy the content from build.")
            print("It will delete it when running the command")
            i1 = input(
                str(Fore.RED+"y for confirm ,Any Other key to cancel "+Fore.WHITE))
            if i1 == "y":
                shutil.rmtree("build")
            elif i1 == "Y":
                shutil.rmtree("build")
            else:
                sys.exit()

        elif i == "ethtemp":
            shutil.rmtree("ethtemp")


def gteethtempjson():
    os.mkdir("ethtemp")
    os.mkdir("ethtemp/json")
    count = 0
    for i in range(0, TotalSupply):
        uri = (f'{BaseUri}/{i}')
        r1 = r.get(uri)
        j1 = json.loads(r1.content)
        f1 = open(f'ethtemp/json/{i}.json', "w+")
        json.dump(j1, f1, indent=2)
        count += 1
        print(Fore.GREEN+(f'{count} JSON done')+Fore.WHITE)


def gethtempimg():
    os.mkdir("ethtemp/image")
    count = 0
    for i in range(0, TotalSupply):
        f1 = jl(open(f'ethtemp/json/{i}.json', "r+"))
        p1 = f1["image"]
        p2=p1.split("://")[0]
        
        if p2=="ipfs":
                p3=p1.split("ipfs://")[-1]
                imgurl=(f'https://opensea.mypinata.cloud/ipfs/{p3}')

        elif p2=="https":
            imgurl=p1



        res = r.get(imgurl, stream=True)

        if res.status_code == 200:
            with open(f'ethtemp/image/{i}.png', 'wb') as f:
                shutil.copyfileobj(res.raw, f)



def build():
    os.mkdir("build")
    os.mkdir("build/json")
    os.mkdir("build/image")
    k1 = os.listdir("ethtemp/image")
    k2 = os.listdir("ethtemp/json")
    l1 = len(k1)
    l2 = len(k2)
    if l1 == TotalSupply:
        if l2 == TotalSupply:
            for i in k1:
                shutil.copy(f'ethtemp/image/{i}', f'build/image/{i}')
            for j in k2:
                shutil.copy(f'ethtemp/json/{j}', f'build/json/{j}')
            print(Fore.YELLOW+str(" Done!! CHeck Build Folder"))


before()
gteethtempjson()
gethtempimg()
build()
