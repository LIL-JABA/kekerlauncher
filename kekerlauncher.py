import os
import json
#import requests
import hashlib
import zipfile
import getpip

SETTINGS_FILE = "settings.json"
URLS_FILE = "urls.json"

def load_globals():
    global settings, urls
    with open(SETTINGS_FILE) as f0, open(URLS_FILE) as f1:
        settings = json.load(f0)
        urls = json.load(f1)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_update():
    load_globals()
    version_url = urls["Miscellaneous"]["version"]
    return settings["Version"] != requests.get(version_url).text

def update():
    load_globals()
    print("Updating KekerLauncher")
    print("KekerLauncher updated successfully. Restarting KekerLauncher.")

def install_pip():
    try:
        import pip
    except ImportError as e:
        getpip.main()


def download_keker(name, download_url, requirements=None, checksum=None):#
    if requirements is not None:
        install_pip()
        get_requirements(requirements)
    if os.path.exists(f"{os.getcwd()}\\{name}.zip"):
        os.remove(f"{os.getcwd()}\\{name}.zip")
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        with open(f"{name}.zip", 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        with open(f"{os.getcwd()}\\{name}.zip", 'rb') as f:
                data = f.read()
                hash_md5 = hashlib.md5(data).hexdigest()
        if hash_md5 == checksum or checksum is None:
            print(f"Keker {name} downloaded successfully.")
        else:
            print(f"Error while trying to download {name}")
        extract_keker(name)
        print(f"Keker {name} downloaded successfully.")
    else:
        print(f"Error while trying to download {name}")

def extract_keker(name):
    if not os.path.exists(os.getcwd()+"\\kekers"):
        os.mkdir("kekers")
    if os.path.exists(f"kekers/{name}"):
        pass
    with zipfile.ZipFile(f"{name}.zip", 'r') as zip_ref:
        zip_ref.extractall("kekers/")
    os.remove(f"{os.getcwd()}\\{name}.zip")
    print(f"Keker {name} extracted successfully.")

def start_keker(name):
    load_globals()
    keker_url = f"https://raw.githubusercontent.com/WeCanCodeTrust/kekerlauncher/main/{name}.md"
    resp = requests.get(keker_url).text.split(" : ")
    download_url, requirements, checksum = resp
    download_keker(name, download_url, requirements, checksum)

def keker_select():
    load_globals()
    clear_console()
    kekerlist = []
    resp = requests.get(urls["Miscellaneous"]["kekers"]).text.split("\n")
    for line in resp:
        if line:
            name, description, maker = line.split(":")
            kekerlist.append((name, description, maker))
    num = 1
    for keker in kekerlist:
        print(num, keker[0])
        num += 1
    while True:
        c = int(input("Which kekers should be run?:\n"))    
        try:
            start_keker(kekerlist[c-1][0])
            break
        except ValueError:
            clear_console()
def get_requirements(requirements):
    reqs_list = []
    reqs  = requests.get(requirements).text.replace("@echo off\n","").replace("pause","").replace("\n","").split("pip install ")
    for req in reqs:
        if req != "":
            reqs_list.append(req)
    print(reqs_list)


def startup():
    load_globals()
    while True:
        if settings["AutoUpdate"] == True:
            if check_update():
                update()
            keker_select()
        elif settings["AutoUpdate"] == False:
            if check_update():
                print("There is a new version available")
            keker_select()
        else:
            while True:
                print("AutoUpdate isn't set. Do you want to check for updates on every startup?")
                autoupdate = input("[Y]es/[N]o: ").lower().strip()
                if autoupdate == "y":
                    settings["AutoUpdate"] = True
                    with open(SETTINGS_FILE, "w") as f:
                        json.dump(settings, f)
                    break
                elif autoupdate == "n":
                    settings["AutoUpdate"] = False
                    with open(SETTINGS_FILE, "w") as f:
                        json.dump(settings, f)
                    break
                else:
                    pass

if __name__ == "__main__":
    startup()