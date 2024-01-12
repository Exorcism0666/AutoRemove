import requests
import pathlib
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import os, sys
urllib3.disable_warnings(InsecureRequestWarning)
import json
import bs4

GH_TOKEN = sys.argv[1]

def report_existed(id: str, Version: str) -> None:
    print(f"{id}: {Version} has already existed, skip publishing")

def komac(path: str, debug: bool = False) -> pathlib.Path:
    Komac = pathlib.Path(path)/"komac.jar"
    if not debug:
        with open(Komac, "wb+") as f:
            file = requests.get("https://gh.xfisxf.top/https://github.com/russellbanks/Komac/releases/download/v1.11.0/Komac-1.11.0-all.jar", verify=False)
            f.write(file.content)
    return Komac

def command(komac: pathlib.Path, id: str, urls: str, version: str, token: str) -> str:
    Commands = "java -jar {} update --id {} --urls {} --version {} --submit --token {}".format(komac.__str__(), id, urls, version, token)
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
         "'": ""
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
    path = pathlib.Path(__file__).parents[0] / "config" / "list.json"
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
    Komac = komac(pathlib.Path(__file__).parents[0], debug)
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
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add HandBrake.HandBrake to Update List
    id = "HandBrake.HandBrake"
    JSON = requests.get("https://api.github.com/repos/HandBrake/HandBrake/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/HandBrake/HandBrake/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("blockmap" in each["browser_download_url"]) and (("arm64" in each["browser_download_url"]) or ("x86_64" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add SchildiChat.SchildiChat to Update List
    id = "SchildiChat.SchildiChat"
    JSON = requests.get("https://api.github.com/repos/SchildiChat/schildichat-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SchildiChat/schildichat-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ".exe" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add cinnyapp.cinny-desktop to Update List
    id = "cinnyapp.cinny-desktop"
    JSON = requests.get("https://api.github.com/repos/cinnyapp/cinny-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/cinnyapp/cinny-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Tyrrrz.DiscordChatExporter.CLI to Update List
    id = "Tyrrrz.DiscordChatExporter.CLI"
    JSON = requests.get("https://api.github.com/repos/Tyrrrz/DiscordChatExporter/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Tyrrrz/DiscordChatExporter/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".Cli.zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Tyrrrz.DiscordChatExporter.GUI to Update List
    id = "Tyrrrz.DiscordChatExporter.GUI"
    JSON = requests.get("https://api.github.com/repos/Tyrrrz/DiscordChatExporter/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Tyrrrz/DiscordChatExporter/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith("ChatExporter.zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Tyrrrz.LightBulb to Update List
    id = "Tyrrrz.LightBulb"
    JSON = requests.get("https://api.github.com/repos/Tyrrrz/LightBulb/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Tyrrrz/LightBulb/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add yt-dlp.yt-dlp to Update List
    id = "yt-dlp.yt-dlp"
    JSON = requests.get("https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not each["browser_download_url"].endswith("min.exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add yt-dlp.yt-dlp.nightly to Update List
    id = "yt-dlp.yt-dlp.nightly"
    JSON = requests.get("https://api.github.com/repos/yt-dlp/yt-dlp-nightly-builds/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/yt-dlp/yt-dlp-nightly-builds/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not each["browser_download_url"].endswith("min.exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Gyan.FFmpeg to Update List
    id = "Gyan.FFmpeg"
    JSON = requests.get("https://api.github.com/repos/GyanD/codexffmpeg/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/GyanD/codexffmpeg/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith("full_build.zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Gyan.FFmpeg.Shared to Update List
    id = "Gyan.FFmpeg.Shared"
    JSON = requests.get("https://api.github.com/repos/GyanD/codexffmpeg/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/GyanD/codexffmpeg/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith("full_build-shared.zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Gyan.FFmpeg.Essentials to Update List
    id = "Gyan.FFmpeg.Essentials"
    JSON = requests.get("https://api.github.com/repos/GyanD/codexffmpeg/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/GyanD/codexffmpeg/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith("essentials_build.zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Obsidian.Obsidian to Update List
    id = "Obsidian.Obsidian"
    JSON = requests.get("https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].startswith("Obsidian.")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add defi.defi to Update List
    id = "defi.defi"
    JSON = requests.get("https://api.github.com/repos/BirthdayResearch/defichain-app/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/BirthdayResearch/defichain-app/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add OleguerLlopart.OpenComic to Update List
    id = "OleguerLlopart.OpenComic"
    JSON = requests.get("https://api.github.com/repos/ollm/OpenComic/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/ollm/OpenComic/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("Portable" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add manosim.gitify to Update List
    id = "manosim.gitify"
    JSON = requests.get("https://api.github.com/repos/gitify-app/gitify/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/gitify-app/gitify/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    
    # Add dscalzi.HeliosLauncher to Update List
    id = "dscalzi.HeliosLauncher"
    JSON = requests.get("https://api.github.com/repos/dscalzi/HeliosLauncher/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/dscalzi/HeliosLauncher/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add ChrisKlimas.Twine to Update List
    id = "ChrisKlimas.Twine"
    JSON = requests.get("https://api.github.com/repos/klembot/twinejs/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/klembot/twinejs/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add B3log.SiYuan to Update List
    id = "B3log.SiYuan"
    JSON = requests.get("https://api.github.com/repos/siyuan-note/siyuan/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/siyuan-note/siyuan/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add DaCosySheeep.FactDownloader to Update List
    id = "DaCosySheeep.FactDownloader"
    JSON = requests.get("https://api.github.com/repos/DaCosySheeep/FactDownloader/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/DaCosySheeep/FactDownloader/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add jcv8000.Codex to Update List
    id = "jcv8000.Codex"
    JSON = requests.get("https://api.github.com/repos/jcv8000/Codex/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/jcv8000/Codex/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add AivarAnnamaa.Thonny to Update List
    id = "AivarAnnamaa.Thonny"
    JSON = requests.get("https://api.github.com/repos/thonny/thonny/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/thonny/thonny/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not(("xxl" in each["browser_download_url"]) or ("py38" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Lauriethefish.QuestPatcher to Update List
    id = "Lauriethefish.QuestPatcher"
    JSON = requests.get("https://api.github.com/repos/Lauriethefish/QuestPatcher/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Lauriethefish/QuestPatcher/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add AppbyTroye.KoodoReader to Update List
    id = "AppbyTroye.KoodoReader"
    JSON = requests.get("https://api.github.com/repos/troyeguo/koodo-reader/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/troyeguo/koodo-reader/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not(("blockmap" in each["browser_download_url"]) or ("Portable" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add clouDr-f2e.rubick to Update List
    id = "clouDr-f2e.rubick"
    JSON = requests.get("https://api.github.com/repos/rubickCenter/rubick/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/rubickCenter/rubick/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("blockmap" in each["browser_download_url"]) and (("x64" in each["browser_download_url"]) or ("ia32" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add IPFS.IPFS-Desktop to Update List
    id = "IPFS.IPFS-Desktop"
    JSON = requests.get("https://api.github.com/repos/ipfs/ipfs-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/ipfs/ipfs-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("blockmap" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add jurplel.qView to Update List
    id = "jurplel.qView"
    JSON = requests.get("https://api.github.com/repos/jurplel/qView/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/jurplel/qView/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add YACReader.YACReader to Update List
    id = "YACReader.YACReader"
    JSON = requests.get("https://api.github.com/repos/YACReader/yacreader/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/YACReader/yacreader/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("winx64-7z.exe" in each["browser_download_url"])]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add KeePassXCTeam.KeePassXC to Update List
    id = "KeePassXCTeam.KeePassXC"
    JSON = requests.get("https://api.github.com/repos/keepassxreboot/keepassxc/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/keepassxreboot/keepassxc/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("msi" in each["browser_download_url"]) and not("sig" in each["browser_download_url"]) or (("-LegacyWindows.msi" in each["browser_download_url"]) or ("DIGEST" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add JanProchazka.dbgate to Update List
    id = "JanProchazka.dbgate"
    JSON = requests.get("https://api.github.com/repos/dbgate/dbgate/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/dbgate/dbgate/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("latest" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add staniel359.muffon to Update List
    id = "staniel359.muffon"
    JSON = requests.get("https://api.github.com/repos/staniel359/muffon/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/staniel359/muffon/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add DuongDieuPhap.ImageGlass to Update List
    id = "DuongDieuPhap.ImageGlass"
    JSON = requests.get("https://api.github.com/repos/d2phap/ImageGlass/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/d2phap/ImageGlass/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add sebescudie.GammaLauncher to Update List
    id = "sebescudie.GammaLauncher"
    JSON = requests.get("https://api.github.com/repos/sebescudie/GammaLauncher/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/sebescudie/GammaLauncher/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Ruben2776.PicView to Update List
    id = "Ruben2776.PicView"
    JSON = requests.get("https://api.github.com/repos/Ruben2776/PicView/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Ruben2776/PicView/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add DEVCOM.LuaJIT to Update List
    id = "DEVCOM.LuaJIT"
    JSON = requests.get("https://api.github.com/repos/DevelopersCommunity/cmake-luajit/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/DevelopersCommunity/cmake-luajit/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Vendicated.Vencord.Canary to Update List
    id = "Vendicated.Vencord.Canary"
    JSON = requests.get("https://api.github.com/repos/Vencord/Installer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Vencord/Installer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "VencordInstallerCli.exe" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Vendicated.Vencord.PTB to Update List
    id = "Vendicated.Vencord.PTB"
    JSON = requests.get("https://api.github.com/repos/Vencord/Installer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Vencord/Installer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "VencordInstallerCli.exe" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Vendicated.Vencord to Update List
    id = "Vendicated.Vencord"
    JSON = requests.get("https://api.github.com/repos/Vencord/Installer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Vencord/Installer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "VencordInstallerCli.exe" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add chylex.DiscordHistoryTracker to Update List
    id = "chylex.DiscordHistoryTracker"
    JSON = requests.get("https://api.github.com/repos/chylex/Discord-History-Tracker/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/chylex/Discord-History-Tracker/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "win-x64.zip" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Ombrelin.PlexRichPresence to Update List
    id = "Ombrelin.PlexRichPresence"
    JSON = requests.get("https://api.github.com/repos/Ombrelin/plex-rich-presence/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Ombrelin/plex-rich-presence/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "exe" in each["browser_download_url"]]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add PurpleI2P.i2pd to Update List
    id = "PurpleI2P.i2pd"
    JSON = requests.get("https://api.github.com/repos/PurpleI2P/i2pd/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/PurpleI2P/i2pd/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "exe" in each["browser_download_url"]]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Tribler.Tribler to Update List
    id = "Tribler.Tribler"
    JSON = requests.get("https://api.github.com/repos/Tribler/tribler/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Tribler/tribler/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "exe" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Retroshare.Retroshare to Update List
    id = "Retroshare.Retroshare"
    JSON = requests.get("https://api.github.com/repos/RetroShare/RetroShare/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/RetroShare/RetroShare/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "exe" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Fly-io.flyctl to Update List
    id = "Fly-io.flyctl"
    JSON = requests.get("https://api.github.com/repos/superfly/flyctl/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/superfly/flyctl/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "zip" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add NextDNS.NextDNS.CLI to Update List
    id = "NextDNS.NextDNS.CLI"
    JSON = requests.get("https://api.github.com/repos/nextdns/nextdns/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/nextdns/nextdns/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("armv5" in each["browser_download_url"]) or ("armv6" in each["browser_download_url"]) or ("armv7" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add AdGuard.dnsproxy to Update List
    id = "AdGuard.dnsproxy"
    JSON = requests.get("https://api.github.com/repos/AdguardTeam/dnsproxy/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/AdguardTeam/dnsproxy/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("arm64" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add AdGuard.AdGuardHome to Update List
    id = "AdGuard.AdGuardHome"
    JSON = requests.get("https://api.github.com/repos/AdguardTeam/AdGuardHome/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/AdguardTeam/AdGuardHome/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("darwin" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Genymobile.scrcpy to Update List
    id = "Genymobile.scrcpy"
    JSON = requests.get("https://api.github.com/repos/Genymobile/scrcpy/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Genymobile/scrcpy/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ".zip" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Frontesque.scrcpy+ to Update List
    id = "Frontesque.scrcpy+"
    JSON = requests.get("https://api.github.com/repos/Frontesque/scrcpy-plus/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Frontesque/scrcpy-plus/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ".exe" in each["browser_download_url"]]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Barry-ran.QtScrcpy to Update List
    id = "Barry-ran.QtScrcpy"
    JSON = requests.get("https://api.github.com/repos/barry-ran/QtScrcpy/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/barry-ran/QtScrcpy/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("ubuntu" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Balena.Etcher to Update List
    id = "Balena.Etcher"
    JSON = requests.get("https://api.github.com/repos/balena-io/etcher/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/balena-io/etcher/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("portable" in each["browser_download_url"]) or ("blockmap" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Balena.BalenaCLI to Update List
    id = "Balena.BalenaCLI"
    JSON = requests.get("https://api.github.com/repos/balena-io/balena-cli/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/balena-io/balena-cli/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ".exe" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add GeekCorner.threema to Update List
    id = "GeekCorner.threema"
    JSON = requests.get("https://api.github.com/repos/GeekCornerGH/threema-for-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/GeekCornerGH/threema-for-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "Threema-For-Desktop-setup" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add OnionShare.OnionShare to Update List
    id = "OnionShare.OnionShare"
    JSON = requests.get("https://api.github.com/repos/onionshare/onionshare/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/onionshare/onionshare/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add quotient-im.Quaternion to Update List
    id = "quotient-im.Quaternion"
    JSON = requests.get("https://api.github.com/repos/quotient-im/Quaternion/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/quotient-im/Quaternion/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add DoltHub.Dolt to Update List
    id = "DoltHub.Dolt"
    JSON = requests.get("https://api.github.com/repos/dolthub/dolt/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/dolthub/dolt/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Armin2208.WindowsAutoNightMode to Update List
    id = "Armin2208.WindowsAutoNightMode"
    JSON = requests.get("https://api.github.com/repos/AutoDarkMode/Windows-Auto-Night-Mode/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/AutoDarkMode/Windows-Auto-Night-Mode/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add xavidop.cxcli to Update List
    id = "xavidop.cxcli"
    JSON = requests.get("https://api.github.com/repos/xavidop/dialogflow-cx-cli/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/xavidop/dialogflow-cx-cli/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("sbom" in each["browser_download_url"]) or ("armv7" in each["browser_download_url"])) and (("arm64" in each["browser_download_url"]) or ("x86_64" in each["browser_download_url"]) or ("i386" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Chocolatey.ChocolateyGUI to Update List
    id = "Chocolatey.ChocolateyGUI"
    JSON = requests.get("https://api.github.com/repos/chocolatey/ChocolateyGUI/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/chocolatey/ChocolateyGUI/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Chocolatey.Chocolatey to Update List
    id = "Chocolatey.Chocolatey"
    JSON = requests.get("https://api.github.com/repos/chocolatey/choco/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/chocolatey/choco/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add ChawyeHsu.Hok to Update List
    id = "ChawyeHsu.Hok"
    JSON = requests.get("https://api.github.com/repos/chawyehsu/hok/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/chawyehsu/hok/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("sha256" in each["browser_download_url"]) and (("aarch64" in each["browser_download_url"]) or ("i686" in each["browser_download_url"]) or ("x86_64" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Ryujinx.Ryujinx.Ava to Update List
    id = "Ryujinx.Ryujinx.Ava"
    JSON = requests.get("https://api.github.com/repos/Ryujinx/release-channel-master/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Ryujinx/release-channel-master/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("sdl2" in each["browser_download_url"]) or ("test" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add TeamIDE.TeamIDE to Update List
    id = "TeamIDE.TeamIDE"
    JSON = requests.get("https://api.github.com/repos/team-ide/teamide/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/team-ide/teamide/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("blockmap" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add CrowTranslate.CrowTranslate to Update List
    id = "CrowTranslate.CrowTranslate"
    JSON = requests.get("https://api.github.com/repos/crow-translate/crow-translate/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/crow-translate/crow-translate/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add kramo.Cartridges to Update List
    id = "kramo.Cartridges"
    JSON = requests.get("https://api.github.com/repos/kra-mo/cartridges/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/kra-mo/cartridges/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add hikari-no-yume.touchHLE to Update List
    id = "hikari-no-yume.touchHLE"
    JSON = requests.get("https://api.github.com/repos/hikari-no-yume/touchHLE/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/hikari-no-yume/touchHLE/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith("Windows_x86_64.zip")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add LIJI32.SameBoy to Update List
    id = "LIJI32.SameBoy"
    JSON = requests.get("https://api.github.com/repos/LIJI32/SameBoy/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/LIJI32/SameBoy/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("cocoa" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Windscribe.Windscribe to Update List
    id = "Windscribe.Windscribe"
    JSON = requests.get("https://api.github.com/repos/Windscribe/Desktop-App/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Windscribe/Desktop-App/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("arm64" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add TeXstudio.TeXstudio to Update List
    id = "TeXstudio.TeXstudio"
    JSON = requests.get("https://api.github.com/repos/texstudio-org/texstudio/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/texstudio-org/texstudio/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Aserto.DSLoad to Update List
    id = "Aserto.DSLoad"
    JSON = requests.get("https://api.github.com/repos/aserto-dev/ds-load/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/aserto-dev/ds-load/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("linux" in each["browser_download_url"]) or ("darwin" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Joplin.Joplin to Update List
    id = "Joplin.Joplin"
    JSON = requests.get("https://api.github.com/repos/laurent22/joplin/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/laurent22/joplin/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("Portable" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Status.Status to Update List
    id = "Status.Status"
    JSON = requests.get("https://api.github.com/repos/status-im/status-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/status-im/status-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add jendrikseipp.RedNotebook to Update List
    id = "jendrikseipp.RedNotebook"
    JSON = requests.get("https://api.github.com/repos/jendrikseipp/rednotebook/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/jendrikseipp/rednotebook/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add moneymanagerex.moneymanagerex to Update List
    id = "moneymanagerex.moneymanagerex"
    JSON = requests.get("https://api.github.com/repos/moneymanagerex/moneymanagerex/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/moneymanagerex/moneymanagerex/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("win32" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add GoXLR-on-Linux.GoXLR-Utility to Update List
    id = "GoXLR-on-Linux.GoXLR-Utility"
    JSON = requests.get("https://api.github.com/repos/GoXLR-on-Linux/goxlr-utility/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/GoXLR-on-Linux/goxlr-utility/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Hugo.Hugo to Update List
    id = "Hugo.Hugo"
    JSON = requests.get("https://api.github.com/repos/gohugoio/hugo/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/gohugoio/hugo/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("extended" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Hugo.Hugo.Extended to Update List
    id = "Hugo.Hugo.Extended"
    JSON = requests.get("https://api.github.com/repos/gohugoio/hugo/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/gohugoio/hugo/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and ("extended" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add tangshimin.MuJing to Update List
    id = "tangshimin.MuJing"
    JSON = requests.get("https://api.github.com/repos/tangshimin/MuJing/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/tangshimin/MuJing/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Alist.Alist to Update List
    id = "Alist.Alist"
    JSON = requests.get("https://api.github.com/repos/alist-org/alist/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/alist-org/alist/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("upx" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add dynobo.NormCap to Update List
    id = "dynobo.NormCap"
    JSON = requests.get("https://api.github.com/repos/dynobo/normcap/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/dynobo/normcap/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Bruno.Bruno to Update List
    id = "Bruno.Bruno"
    JSON = requests.get("https://api.github.com/repos/usebruno/bruno/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/usebruno/bruno/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add SoftFever.OrcaSlicer to Update List
    id = "SoftFever.OrcaSlicer"
    JSON = requests.get("https://api.github.com/repos/SoftFever/OrcaSlicer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SoftFever/OrcaSlicer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add IPEP.Scantailor-Experimental to Update List
    id = "IPEP.Scantailor-Experimental"
    JSON = requests.get("https://api.github.com/repos/ImageProcessing-ElectronicPublications/scantailor-experimental/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/ImageProcessing-ElectronicPublications/scantailor-experimental/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("X86-64-Qt6" in each["browser_download_url"])]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add nzbget.nzbget to Update List
    id = "nzbget.nzbget"
    JSON = requests.get("https://api.github.com/repos/nzbgetcom/nzbget/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/nzbgetcom/nzbget/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("debug" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add RustDesk.RustDesk to Update List
    id = "RustDesk.RustDesk"
    JSON = requests.get("https://api.github.com/repos/rustdesk/rustdesk/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/rustdesk/rustdesk/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add LutzRoeder.Netron to Update List
    id = "LutzRoeder.Netron"
    JSON = requests.get("https://api.github.com/repos/lutzroeder/netron/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/lutzroeder/netron/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add SagerNet.sing-box to Update List
    id = "SagerNet.sing-box"
    JSON = requests.get("https://api.github.com/repos/SagerNet/sing-box/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SagerNet/sing-box/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("amd64v3" in each["browser_download_url"]) or ("universal" in each["browser_download_url"]) or ("legacy" in each["browser_download_url"])) and (("arm64" in each["browser_download_url"]) or ("amd64" in each["browser_download_url"]) or ("386" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add gopass.gopass to Update List
    id = "gopass.gopass"
    JSON = requests.get("https://api.github.com/repos/gopasspw/gopass/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/gopasspw/gopass/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add gopass.gopass-jsonapi to Update List
    id = "gopass.gopass-jsonapi"
    JSON = requests.get("https://api.github.com/repos/gopasspw/gopass-jsonapi/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/gopasspw/gopass-jsonapi/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("armv6" in each["browser_download_url"]) or ("armv7" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add AGSProjectTeam.AdventureGameStudio to Update List
    id = "AGSProjectTeam.AdventureGameStudio"
    JSON = requests.get("https://api.github.com/repos/adventuregamestudio/ags/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/adventuregamestudio/ags/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add TailwindLabs.TailwindCSS to Update List
    id = "TailwindLabs.TailwindCSS"
    JSON = requests.get("https://api.github.com/repos/tailwindlabs/tailwindcss/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/tailwindlabs/tailwindcss/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Alex313031.Thorium.AVX2 to Update List
    id = "Alex313031.Thorium.AVX2"
    JSON = requests.get("https://api.github.com/repos/Alex313031/Thorium-Win-AVX2/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Alex313031/Thorium-Win-AVX2/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add HTTPie.HTTPie to Update List
    id = "HTTPie.HTTPie"
    JSON = requests.get("https://api.github.com/repos/httpie/desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/httpie/desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("blockmap" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add squalou.google-chat-linux to Update List
    id = "squalou.google-chat-linux"
    JSON = requests.get("https://api.github.com/repos/squalou/google-chat-linux/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/squalou/google-chat-linux/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add mikf.gallery-dl to Update List
    id = "mikf.gallery-dl"
    JSON = requests.get("https://api.github.com/repos/mikf/gallery-dl/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/mikf/gallery-dl/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("sig" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add houmain.keymapper to Update List
    id = "houmain.keymapper"
    JSON = requests.get("https://api.github.com/repos/houmain/keymapper/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/houmain/keymapper/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add printfn.fend to Update List
    id = "printfn.fend"
    JSON = requests.get("https://api.github.com/repos/printfn/fend/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/printfn/fend/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "windows" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add gaphor.gaphor to Update List
    id = "gaphor.gaphor"
    JSON = requests.get("https://api.github.com/repos/gaphor/gaphor/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/gaphor/gaphor/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("portable" in each["browser_download_url"])]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # # Add Nostalgia-09.AeroChat to Update List
    # id = "Nostalgia-09.AeroChat"
    # JSON = requests.get("https://api.github.com/repos/Nostalgia-09/AeroChat/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    # Version = requests.get("https://api.github.com/repos/Nostalgia-09/AeroChat/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    # Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    # if not version_verify(Version, id):
        # report_existed(id, Version)
    # elif do_list(id, Version, "verify"):
        # report_existed(id, Version)
    # else:
        # Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    # del JSON, Urls, Version, id

   # Add oxen-io.lokinet to Update List
    id = "oxen-io.lokinet"
    JSON = requests.get("https://api.github.com/repos/oxen-io/lokinet/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/oxen-io/lokinet/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add HiroshibaKazuyuki.VOICEVOX to Update List
    id = "HiroshibaKazuyuki.VOICEVOX"
    JSON = requests.get("https://api.github.com/repos/VOICEVOX/voicevox/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/VOICEVOX/voicevox/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("cpu" in each["browser_download_url"]) or ("macos" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add HiroshibaKazuyuki.VOICEVOX.CPU to Update List
    id = "HiroshibaKazuyuki.VOICEVOX.CPU"
    JSON = requests.get("https://api.github.com/repos/VOICEVOX/voicevox/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/VOICEVOX/voicevox/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("directml" in each["browser_download_url"]) or ("macos" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add y-chan.SHAREVOX to Update List
    id = "y-chan.SHAREVOX"
    JSON = requests.get("https://api.github.com/repos/SHAREVOX/sharevox/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SHAREVOX/sharevox/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("cpu" in each["browser_download_url"]) or ("macos" in each["browser_download_url"]) or ("nvidia" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add y-chan.SHAREVOX.CPU to Update List
    id = "y-chan.SHAREVOX.CPU"
    JSON = requests.get("https://api.github.com/repos/SHAREVOX/sharevox/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SHAREVOX/sharevox/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("directml" in each["browser_download_url"]) or ("macos" in each["browser_download_url"]) or ("nvidia" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add y-chan.SHAREVOX.NVIDIA to Update List
    id = "y-chan.SHAREVOX.NVIDIA"
    JSON = requests.get("https://api.github.com/repos/SHAREVOX/sharevox/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SHAREVOX/sharevox/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("directml" in each["browser_download_url"]) or ("macos" in each["browser_download_url"]) or ("cpu" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add SpikeHD.Dorion to Update List
    id = "SpikeHD.Dorion"
    JSON = requests.get("https://api.github.com/repos/SpikeHD/Dorion/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SpikeHD/Dorion/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add XmirrorSecurity.OpenSCA-cli to Update List
    id = "XmirrorSecurity.OpenSCA-cli"
    JSON = requests.get("https://api.github.com/repos/XmirrorSecurity/OpenSCA-cli/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/XmirrorSecurity/OpenSCA-cli/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("sha256" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add DEVCOM.JMeter to Update List
    id = "DEVCOM.JMeter"
    JSON = requests.get("https://api.github.com/repos/DevelopersCommunity/cmake-jmeter/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/DevelopersCommunity/cmake-jmeter/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Nethermind.Nethermind to Update List
    id = "Nethermind.Nethermind"
    JSON = requests.get("https://api.github.com/repos/NethermindEth/nethermind/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/NethermindEth/nethermind/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("linux" in each["browser_download_url"]) or ("macos" in each["browser_download_url"]) or ("assemblies" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add lucasg.Dependencies to Update List
    id = "lucasg.Dependencies"
    JSON = requests.get("https://api.github.com/repos/lucasg/Dependencies/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/lucasg/Dependencies/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("x64" in each["browser_download_url"]) or ("Debug" in each["browser_download_url"]) or ("without" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add PhapDieuDuong.ExifGlass to Update List
    id = "PhapDieuDuong.ExifGlass"
    JSON = requests.get("https://api.github.com/repos/d2phap/ExifGlass/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/d2phap/ExifGlass/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add GAM-Team.GotYourBack to Update List
    id = "GAM-Team.GotYourBack"
    JSON = requests.get("https://api.github.com/repos/GAM-team/got-your-back/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/GAM-team/got-your-back/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add taers232c.GAMADV-XTD3 to Update List
    id = "taers232c.GAMADV-XTD3"
    JSON = requests.get("https://api.github.com/repos/taers232c/GAMADV-XTD3/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/taers232c/GAMADV-XTD3/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Aserto.Topaz to Update List
    id = "Aserto.Topaz"
    JSON = requests.get("https://api.github.com/repos/aserto-dev/topaz/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/aserto-dev/topaz/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("linux" in each["browser_download_url"]) or ("darwin" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add UniversalMediaServer.UniversalMediaServer to Update List
    id = "UniversalMediaServer.UniversalMediaServer"
    JSON = requests.get("https://api.github.com/repos/UniversalMediaServer/UniversalMediaServer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/UniversalMediaServer/UniversalMediaServer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Canonical.Multipass to Update List
    id = "Canonical.Multipass"
    JSON = requests.get("https://api.github.com/repos/canonical/multipass/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/canonical/multipass/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add AppFlowy.AppFlowy to Update List
    id = "AppFlowy.AppFlowy"
    JSON = requests.get("https://api.github.com/repos/AppFlowy-IO/AppFlowy/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/AppFlowy-IO/AppFlowy/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add errata-ai.Vale to Update List
    id = "errata-ai.Vale"
    JSON = requests.get("https://api.github.com/repos/errata-ai/vale/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/errata-ai/vale/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Jubler.App to Update List
    id = "Jubler.App"
    JSON = requests.get("https://api.github.com/repos/teras/Jubler/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/teras/Jubler/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Task.Task to Update List
    id = "Task.Task"
    JSON = requests.get("https://api.github.com/repos/go-task/task/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/go-task/task/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and (("arm64" in each["browser_download_url"]) or ("amd64" in each["browser_download_url"]) or ("386" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add calibre.calibre to Update List
    id = "calibre.calibre"
    JSON = requests.get("https://api.github.com/repos/kovidgoyal/calibre/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/kovidgoyal/calibre/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("portable" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Updating
    if not debug:
        for each in Commands:
            if os.system(each[0]) == 0:
                do_list(*each[1])
    
    # Cleanup the merged branch
    os.system(f"java -jar {Komac} branch cleanup --only-merged --token {GH_TOKEN}")

    return Commands

if __name__ == "__main__":
    print([each[0] for each in main()])
