import pathlib
import sys
import re
import time

PATH = pathlib.Path(__file__).parents[1] / "Changelog.md"
Status = sys.argv[1]

if re.match("[S|s]uccess", Status):
    with open(PATH, "a+", encoding="utf-8") as f:
        f.write(f"- Running at {time.strftime('%Y-%m-%d %H:%M:%S')} has been successful\n")
elif re.match("[F|f]ail", Status):
    with open(PATH, "a+", encoding="utf-8") as f:
        f.write(f"- Running at {time.strftime('%Y-%m-%d %H:%M:%S')} has been fail\n")
else:
    raise Exception
