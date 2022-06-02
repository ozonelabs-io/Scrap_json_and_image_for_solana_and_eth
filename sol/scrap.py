import json
import os
import shutil
from colorama import Fore
import requests as r
import subprocess


hashaddr = "FgaPTE1tH6AvBtxgeUeTTRgRpXeyM6KceRkeSGEs5rCF"


def hashlist():
    f1 = subprocess.run(
        f"metaboss snapshot mints -c {hashaddr} -t 120", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    d1 = f1.stdout.decode('utf-8')
    d2 = f1.stderr.decode('utf-8')

    if "Done!" in d1:
        print(Fore.LIGHTGREEN_EX+"hashlist done"+Fore.WHITE)

    if "error" in d2:
        print(Fore.LIGHTMAGENTA_EX+"please reun again"+Fore.WHITE)
    t1 = os.listdir()
    for i in t1:
        if i == "hashlist.json":
            os.remove("hashlist.json")

    os.rename(f'{hashaddr}_mint_accounts.json', "hashlist.json")


def confirmation():
    f1 = os.listdir()
    for i in f1:
        if i == "temp":
            shutil.rmtree("temp")

        elif i == "buildtemp":
            shutil.rmtree("buildtemp")

        elif i == "build":
            f2 = open("hashlist.json")
            f3 = json.load(f2)
            f4 = len(f3)
            f5 = os.listdir("build/png")
            f6 = len(f5)
            if f4 != f6:
                shutil.rmtree("build")

            elif f4 == f6:
                print(Fore.LIGHTBLUE_EX+"\nBuild Folder Already Exist... ")
                print("Do You Wants To Continue However."+Fore.WHITE)
                f7 = input(
                    Fore.RED+' "Y" For YES,"N" for NO ..... ' + Fore.WHITE)
                if f7 == "Y":
                    shutil.rmtree("Build")
                elif f7 == "y":
                    shutil.rmtree("Build")
                else:
                    break


def snapshoturi():
    # 1
    l = []
    f1 = open("hashlist.json", "r+")
    f2 = json.load(f1)

    os.mkdir("temp")
    os.mkdir("temp/hashdecode")
    cmd = "metaboss decode mint -L hashlist.json -o temp/hashdecode -t 120 "
    sp = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    d1 = sp.stdout.decode('utf-8')
    d2 = sp.stderr.decode('utf-8')

    if "Using a public RPC URL" in d1:
        print(Fore.RED+"\nIf you want you can use your own cutom rpc url if you have...."+Fore.WHITE)

    if "Decoding accounts..." in d1:
        print(Fore.GREEN +
              "\nDecoding Done\n"+Fore.WHITE)

    if "error" in d2:
        print(Fore.MAGENTA+"Pease close the terminal and rerun it\n make sure you are connected wth internet"+Fore.WHITE)


def scrapdata():
    # 2
    f1 = os.listdir("temp/hashdecode")
    os.mkdir("temp/json")
    count = 0
    for i in f1:

        m1 = open(f'temp/hashdecode/{i}', "r+")
        m2 = json.load(m1)

        url = m2["uri"]
        f1 = r.get(url)
        f2 = json.loads(f1.content)

        f3 = open(f'temp/json/{i}', "w+")
        f5 = json.dump(f2, f3, sort_keys=True, indent=2)
        count += 1
        print(Fore.GREEN+f'{count} Temp Json Done!!'+Fore.WHITE)


def image():
    # 3
    os.mkdir("temp/image")
    f1 = os.listdir("temp/json")
    count = 0
    print("\n")
    for i in f1:
        f1 = open(f'temp/json/{i}', "r+")
        f2 = json.load(f1)
        url = f2["image"]
        name = (i.split(".json")[0])+".png"

        res = r.get(url, stream=True)

        if res.status_code == 200:
            with open(f'temp/image/{name}', 'wb') as f:
                shutil.copyfileobj(res.raw, f)
                count += 1

        print(Fore.CYAN+f'{count} Temp Png Done!!')


def dropbuild():
    # 4
    os.mkdir("build")
    os.mkdir("build/json")
    os.mkdir("build/tempjson")

    shutil.copytree(f"temp/image", f'build/png')
    f1 = os.listdir("temp/json")
    for i in f1:
        f2 = json.load(open(f"temp/json/{i}", "r+"))
        bname = f2["name"].split("#")[-1]
        imgname = (i.split(".json")[0])+".png"
        shutil.copy(f"temp/json/{i}", f'build/tempjson/{bname}.json')
        os.rename(f'build/png/{imgname}', f'build/png/{bname}.png')

    p1 = os.listdir("build/tempjson")
    for j in p1:
        t1 = json.load(open(f'build/tempjson/{j}', "r+"))
        numpng = j.split(".json")[0]+".png"
        t1["image"] = numpng
        t1["properties"]["files"][0]["uri"] = numpng
        t2 = open(f"build/json/{j}", "w+")
        json.dump(t1, t2)

    g1 = os.listdir("build/tempjson")
    g2 = os.listdir("build/json")

    n1 = len(g1)
    n2 = len(g2)
    if n1 == n2:
        shutil.rmtree("build/tempjson")
    print(
        Fore.GREEN+"All done check the build folder for The generated image and json\n"+Fore.WHITE)
    exit()


hashlist()
confirmation()
snapshoturi()
scrapdata()
image()
dropbuild()
