import requests
import os, sys
import pathlib
import yaml
import threading
import time
import random

token = sys.argv[1]
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47"
}

def Komac(path: str, debug: bool = False) -> pathlib.Path:
    Komac = pathlib.Path(path)/"komac.jar"
    if not debug:
        with open(Komac, "wb+") as f:
            file = requests.get("https://gh.api-go.asia/https://github.com/russellbanks/Komac/releases/download/v1.10.1/Komac-1.10.1-all.jar", verify=False)
            f.write(file.content)
    return Komac
komac = Komac(pathlib.Path(__file__).parents[0])
def command_generator(token: str, id: str, version: str, reason: str, komac_path: pathlib.Path, java_path: pathlib.Path = pathlib.Path("java")) -> bool:
    return f"{java_path} -jar {komac_path} remove --id {id} --version {version} --reason '{reason}' --submit --token {token}"

def scan(_yaml: dict, token: str):
    id = _yaml["PackageIdentifier"]
    version = _yaml["PackageVersion"]
    url_list: list = _yaml["Installers"]
    try:
        for each in url_list:
            print(f"Starting check {id}")
            code = requests.get(each["InstallerUrl"], headers=headers).status_code
            if code >= 400:
                command = command_generator(token, id, version, f"[Automated] It returns {code} code in architecture {each['Architecture']}", komac)
                os.system(command)
                print(f"{id} checks fail, running", command)
                break
        else:
            print(f"{id} checks successful")
    except BaseException:
        print(f"{id} checks bad")


def scanner(path: pathlib.Path, token: str):
    for each in os.listdir(path):
        _path = path / each
        if _path.is_dir():
            scanner(_path, token)
        elif _path.is_file():
            if ".installer.yaml" in _path.name:
                _yaml = each / _path
                with open(_yaml, "r", encoding="utf-8") as f:
                    yaml_ = yaml.load(f.read(), yaml.FullLoader)
                    scan(yaml_, token)

def main():
    # global search winget-pkgs folder
    origin: list[pathlib.Path] = []
    for each in pathlib.Path(__file__).parents:
        if len(origin) > 0:
            break
        origin = [each / i / "manifests" for i in os.listdir(each) if "winget-pkgs" in i]
    if len(origin) == 0:
        raise Exception("Cannot find winget-pkgs folder")
    folder = origin[0]
    del origin
    print(f"We've found the folder in {folder}")

    # scan
    target = []
    while len(target) <= 3:
        _target = []
        for each in range(1, random.randint(3, 5)):
            _target.append(os.listdir(folder)[random.randint(1, len(os.listdir(folder)) - 1)])

        target = [folder / pathlib.Path(t) for t in list(set(_target))]
    
    for t in target:
        scanner(t, token)


if __name__ == "__main__":
    runner = threading.Thread(target=main)
    runner.start()
    for each in range(1, 2*60*60):
        if not runner.is_alive():
            break
        time.sleep(1)
    print("scanning timeout, safely exiting......")
    exit(0)