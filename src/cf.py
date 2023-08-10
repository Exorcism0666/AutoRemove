import requests
from os import system
from sys import argv

Token = argv[1]

for each in range(1, 8):
    JSON = requests.get(f"https://api.github.com/repos/JetBrains/kotlin/releases?page={each}", verify=False).json()
    for each in JSON:
        try:
            Version = each["tag_name"].replace('v', '')
            if "build" in Version:
                continue
            URLs = [i["browser_download_url"] for i in each["assets"] if "compiler" in i["browser_download_url"] and i["browser_download_url"][-4::] == ".zip"]
            URLs = str(URLs).replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
            print(f"java -jar Komac-1.9.1-all.jar up --id JetBrains.Kotlin.Compiler --version {Version} --urls {URLs} --submit")
            system(f"java -jar Komac-1.9.1-all.jar --id JetBrains.Kotlin.Compiler --version {Version} --urls {URLs} --submit --token {Token}")
        except BaseException as e:
            print(e)
