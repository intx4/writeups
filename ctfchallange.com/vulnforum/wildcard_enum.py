import subprocess

cmd = 'dnsrecon --iw -D ~/ctf/ctfchallenge/subdomains.txt -d auth.vulnforum.co.uk -t brt'

result = subprocess.getoutput(cmd)
lines = result.split("[*]")
entries = []

for l in lines:
    l = l.strip("\n\t ")
    if "[!]" in l or "[+]" in l:
        continue
    if "A" in l or "CNAME" in l or "NS" in l:
        entries.append(l)

iw = "68.183.255.206" #default wildcard IP

for i,entry in enumerate(entries):
    if "CNAME" in entry:
        continue
    if "A" in entry:
        if iw not in entry:
            print(i)
            print("[?] " + entries[i-1] + "\n")
            print("[?] " + entry)
