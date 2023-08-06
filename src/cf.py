import requests
from os import system
from sys import argv

Token = argv[1]

for each in range(1, 6):
    JSON = requests.get("https://api.github.com/repos/cloudflare/cloudflared/releases", verify=False).json()
    for each in JSON[::-1]:
        try:
            Version = each["tag_name"]
            URLs = [i["browser_download_url"] for i in each["assets"] if ".msi" in i["browser_download_url"]]
            print(f"Komac up --id Cloudflare.cloudflared --version {Version} --urls {URLs[0]},{URLs[1]} --submit")
            system(f"Komac up --id Cloudflare.cloudflared --version {Version} --urls {URLs[0]},{URLs[1]} --submit --token {Token}")
        except BaseException as e:
            print(e)
