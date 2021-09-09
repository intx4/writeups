# nslookup
We have an MX entry (mail) : `hostmaster.vulnlawyers.co.uk`
# dnsrecon
`dnsrecon -d vulnlawyers.co.uk -D ~/ctf/ctfchallenge/vulnlawyers/subdomains.txt`
Nothing useful. Only subdoman is www.
Apparently it uses the Authoritative server for this.
`dnsrecon -d vulnlawyers.co.uk -D ~/ctf/ctfchallenge/vulnlawyers/subdomains.txt -t brt -n 8.8.8.8`
There's an A entry: `data.vulnlawyers.co.uk`
# data subdomain
There's the first flag.
With ffuf for content discovery -> there is an endpoint `/users`
There is a flag and some emails. 
# ffuf
`ffuf -t 1 -p 0.1 -mc all -u http://www.vulnlawyers.co.uk/FUZZ -w contents.txt -H "Cookie: ctfchallenge=eyXXX" -fc 404`
We find:
- /css 403
- /images 403
- /js 403
- /login 302 (redirect)
- /denied 401 (denied)

/login redirects to /denied which responds to GET with 401 (not authorized).

# /login
with `curl`, we bypass the 401 status (curl does not follow the redirection (302) by default). In the page we find a new link to an entrypoint for logging in `/lawyers-only` and a flag.

# credentials bruteforcing
See `login.py` for email retrievals plus password bruteforcing.
We manage to access as one of the people. We see that there's a case managed by shayne (or whatever).
Trying to bruteforce the password with ffuf brings no results
# IDOR
One of the pages we can visit when logged in is the profile: `/lawyers-only-profile`. Examining the requests the url is `/lawyers-only-profile-details/4` -> change ID to obtain shayne password.
# End
We log in as shayne, delete case, get last flag.
