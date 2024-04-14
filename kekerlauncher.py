import os
import json
import requests
#
#
#
def load_globals():
    global settings,urls
    with open("settings.json") as f0 ,open("urls.json") as f1:
        settings = json.load(f0)
        urls = json.load(f1)
#
#
#
def clear_console(): # clears the console with the coresponding command for it (its diffrent from os)
    os.system('cls' if os.name == 'nt' else 'clear')
#
#
#
def check_update(): # checks if there is a new version of the launcher
    if settings["Version"] == requests.get(urls["Miscellaneous"]["version"]).text:
        return False
    
    else:
        return True
#
#
#
def update(): # updates launcher
    pass
#
#
#
def keker_select(): # let u select a keker
    pass
#
#
#
def get_kekers(): # gets all avabile kekers as well as theyre requiremtents checksum and download links
    load_globals()
    kekerlist = []
    kekers = requests.get(settings["Miscellaneous"]["kekers"]).text.split(":")
    for keker,descripton,creator in kekers:
        print(f"kekername: {keker} | {descripton} | made by {creator}")
        kekerlist.append(keker[descripton,creator])
    print(kekerlist)
#
#
#
def startup(): # startup combindes all the functions could get replaced with a gui version to
    clear_console()
    load_globals()
    while True:
        if settings["AutoUpdate"] == True:
            if check_update() == True:
                update()

            get_kekers()
            keker_select()
        
        elif settings["AutoUpdate"] == False:
            if check_update() == True:
                print("There is a new Version Aviable")

            get_kekers()
            keker_select()

        else:
            while True:
                print("AutoUpdate isnt set You want to check for updates on every startup?")
                autoupdate = input("[Y]es/[N]o: ").lower().removesuffix("es"or"o") 
                if autoupdate == "y":
                    settings["AutoUpdate"] = True # set the AutoUpdate to True {"AutoUpdate":true}
                    with open("settings.json", "w") as f:
                        json.dump(settings, f) # writes it into the file {"AutoUpdate":true}

                    break

                elif autoupdate == "n":
                    settings["AutoUpdate"] = False # set the AutoUpdate to False {"AutoUpdate":false}
                    with open("settings.json", "w") as f:
                        json.dump(settings, f)

                    break

                else:
                    clear_console()
#
#
#
startup()