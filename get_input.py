import os
import datetime
import requests

now = datetime.datetime.now()
newfilepath = os.path.join(os.path.dirname(__file__), str(now.year), f"day{now.day:02}.txt")

session = open(os.path.join(os.path.dirname(__file__), "sessioncookie.txt")).read().strip()

link = f"https://adventofcode.com/{now.year}/day/{now.day}/input"

txt = requests.get(link, cookies={"session":session}).text

with open(newfilepath, "w+") as f:
    f.write(txt[:-1])

