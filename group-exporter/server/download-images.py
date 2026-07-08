from constants import IMAGES_FOLDER, JSON_FILE
import requests
import time
import json

print("Cookies are needed. This script will download all images from all logins.")
print(
    'You can obtain your cookies by simply typing "document.cookie" in your JS console and pasting the result here.'
)
cookies = input("Cookies: ")

users = []

with open(JSON_FILE, "r") as f:
    content = json.loads(f.read())

    for module in content:
        for project in content[module]:
            for group in content[module][project]:
                users.append(group["master"]["login"])
                for member in group["members"]:
                    users.append(member["login"])

users = list(set(users))

BASE_URL = "https://intra.epitech.eu/file/userprofil/commentview"

for user in users:
    r = requests.get(
        f"{BASE_URL}/{user}.jpg",
        headers={
            "Accept": "image/avif,image/jxl,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
            "Cookie": cookies,
            "User-Agent": "Mozilla/5.0 (U; Linux x86_64; en-US) Gecko/20100101 Firefox/149.0",
        },
    )
    with open(f"{IMAGES_FOLDER}/{user}.jpg", "wb+") as f:
        f.write(r.content)
        print(f"Downloaded {user}")
    time.sleep(1)
