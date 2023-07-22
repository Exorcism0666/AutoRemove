import requests
import os
import sys
import pathlib

token = sys.argv[1]

#how your features of code, It can help people better understand your code, And it would help you to realize your own code

headers = {
    "Authorization": f"Bearer {token}"
}

def komac(path: str, debug: bool = False):
    Komac = pathlib.Path(path)/"komac.jar"
    if not debug:
        with open(Komac, "wb+") as f:
            file = requests.get("https://gh.api-go.asia/https://github.com/russellbanks/Komac/releases/download/v1.9.0/Komac-1.9.0-all.jar", verify=False)
            f.write(file.content)
    return Komac

Komac = komac(pathlib.Path(__file__).parents[0])

for page in range(1, 6):
    JSONs = requests.get(f"https://api.github.com/repos/cloudflare/cloudflared/releases?page={page}", headers=headers, verify=False).json()
    for JSON in JSONs:
        Version = JSON["tag_name"]
        URLs = str([each["browser_download_url"] for each in JSON["assets"] if "msi" in each["browser_download_url"]]).replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        print(URLs, Version)
        Command = f"""java "-Djava.net.useSystemProxies=true" -jar "{Komac}" update --id Cloudflare.cloudflared --urls {URLs} --version {Version} --submit --token {token}"""
        os.system(Command)
        print(Command)
