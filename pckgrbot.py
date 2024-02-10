import requests
import pathlib
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import os, sys
urllib3.disable_warnings(InsecureRequestWarning)
import json
import bs4
import re

GH_TOKEN = sys.argv[1]

def report_existed(id: str, Version: str) -> None:
    print(f"{id}: {Version} has already existed, skip publishing")

def wingetcreate(path: str, debug: bool = False) -> pathlib.Path:
    Wingetcreate = pathlib.Path(path)/"wingetcreate.exe"
    if not debug:
        with open(Wingetcreate, "wb+") as f:
            file = requests.get("https://github.com/microsoft/winget-create/releases/download/v1.5.7.0/wingetcreate.exe", verify=False)
            f.write(file.content)
    return Wingetcreate

def command(wingetcreate: pathlib.Path, urls: str, version: str, id: str, token: str) -> str:
    Commands = "{} update --submit --urls {} --version {} {} --submit --token {}".format(wingetcreate.__str__(), urls, version, id, token)
    return Commands

def clean_string(string: str, keywords: dict[str, str]) -> str:
    for k in keywords:
        string = string.replace(k, keywords[k])
    return string

def str_pop(string: str, index: int) -> str:
        i = list(string)
        i.pop(index)
        i = "".join(i)

        return i

def list_to_str(List: list) -> str:
    new = str(List)
    new = clean_string(new, {
         "[": "",
         "]": "",
         " ": "",
         "'": "",
         ",": " "
    })
    return new

def version_verify(version: str, id: str) -> bool:
    # if len([v for v in requests.get(f"https://winget.vercel.app/api/winget-pkg-versions?pkgid={id}").json()[id] if v == version]) > 0:
    #     return False
    # else:
    return True # always returns true due to that the api has stopped by unknown issue

def do_list(id: str, version: str, mode: str) -> bool | None:
    """
    Mode: write or verify
    """
    path = pathlib.Path(__file__).parents[0] / "config" / "listpckgr.json"
    with open(path, "r", encoding="utf-8") as f:
        try:
            JSON: dict[str, list[str]] = json.loads(f.read())
        except BaseException:
            JSON: dict[str, list[str]] = {}
        if id not in JSON:
            JSON[id] = []
        
        if mode == "write":
            if version not in JSON[id]:
                JSON[id].append(version)
            with open(path, "w+", encoding="utf-8") as w:
                w.write(json.dumps(JSON))
        elif mode == "verify":
            if version in JSON[id]:
                return True
            else:
                return False
        else:
            raise Exception
 
def main() -> list[tuple[str, tuple[str, str, str]]]:
    Commands:list[tuple[str, tuple[str, str, str]]] = []
    debug = bool([each for each in sys.argv if each == "debug"])
    Winegtcreate = wingetcreate(pathlib.Path(__file__).parents[0], debug)
    Headers = [{
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
    }, {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        "Authorization": f"Bearer {GH_TOKEN}"
    }]

# Add Peppy.Osu! to Update List
    id = "Peppy.Osu!"
    JSON = requests.get("https://api.github.com/repos/ppy/osu/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/ppy/osu/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ".exe" in each["browser_download_url"]]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Wingetcreate, list_to_str(Urls), Version, id, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Updating
    if not debug:
        for each in Commands:
            if os.system(each[0]) == 0:
                do_list(*each[1])

    return Commands

if __name__ == "__main__":
    print([each[0] for each in main()])
