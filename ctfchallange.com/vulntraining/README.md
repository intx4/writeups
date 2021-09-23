# Domain discovery
` dnsrecon -d vulntraining.co.uk -D /home/intx/ctf/ctfchallenge/subdomains.txt -n 8.8.8.8 -t brt`

Sub-domains found:
- billing -> login (no luck with bruteforcing)
- admin -> 401 unauthorized (/admin, /invoices)
- www -> look next session

With crt.sh enumaretion we find also `c867fc3a.vulntraining.co.uk` which gives the first flag.

# Endpoints enum on www
`ffuf -t 1 -p 0.1 -mc all -u http://www.vulntraining.co.uk/FUZZ -w ../contents.txt -H "Cookie: ctfchallenge=$(cat ../cookie.txt)" -fc 404`

We find the following:
- .git                    [Status: 403, Size: 170, Words: 5, Lines: 7]
- .git/HEAD               [Status: 200, Size: 23, Words: 2, Lines: 2]
- .git/config             [Status: 200, Size: 288, Words: 19, Lines: 12]
- .git/index              [Status: 200, Size: 1381, Words: 8, Lines: 7]
- css                     [Status: 301, Size: 178, Words: 6, Lines: 8]
- framework               [Status: 301, Size: 178, Words: 6, Lines: 8]
- js                      [Status: 301, Size: 178, Words: 6, Lines: 8]
- robots.txt              [Status: 200, Size: 42, Words: 3, Lines: 2]
- server                  [Status: 302, Size: 3263, Words: 1457, Lines: 109]

Curling into server gives the 4th flag. We skipped 2...
Also going to the github repo listed in the config file gives the 6th flag...

# home source code
Scraping the home website source code we find two flags. One is directly in the html, the other can be found in `/css/style.css`. There is a link to an image. If we explore the directory we find a flat.txt

# robots.txt
I forgot about checking the robots.txt file. We discover an hidden directory that gives the second flag

# Recap
So we have all the first six flags

# GitHub repo

- index.php: includes and evals the php files in the main directory, then calls Route::load() and run()
- Route.php :
    load() : includes and evals url.php in routes/ -> this adds to the routes array a key "GET" associated to (regex = "/^\/[\/]?$" and func="ExampleController@test")
    run() : basically checks if we are visiting the route with an url that matches the route regex. If so it performs the action given in the route function.

- checking the repo history we see some credentials that were removed

# /php-my-s3cret-admin
Curling into /server we see a link to this login form. If we use the credentials listed into the repo we get access to the admin page. Checking the vulntraining table we get the flag.
We find also a user:
    username = dominic.bryant
    password = NDliYmZkNGE4ZWFiNDNlM2Y2MjM3NzQwMmZjZDFkZTQ2MzA0OWZhNTZjZGJhNmNmN2ZmYzVkNWNiYWY0ZjZhNDRiMjU0NDAxZDQ0... -> this must be an hash of somekind

# bruteforcing billing part 2
ffuf -w passwords.txt -X POST -d username=dominic.bryant&password=FUZZ" -t 1 -p 0.1 -H "Cookie: ctfchallenge=eyJkYXRhIjoiZXlKMWMyVnlYMmhoYzJnaU9pSjZibkZrYnpJMmVpSXNJbkJ5WlcxcGRXMGlPbVpoYkhObGZRPT0iLCJ2ZXJpZnkiOiI4ZTA0YTYwMDM2MDUzNjNjOTg4MDY5Yzk1YTMwMzVkNSJ9" -H "Content-Type: application/x-www-form-urlencoded" -u http://billing.vulntraining.co.uk/login -fr "Password is invalid"
` we find the password 987654321

# content discovery in vulnbilling
Nothing apart `/i` for i in (1,5)

# params fuzzing in vulnbilling
If we include 500 server error in the responses, if we get `/?api=x` we get an api error.
We can trigger a SSRF by passing as api an url we are controlling (for example using burp collaborator). We get a flag and a "X-Token: 71e8b37bdc4c8edbf197d42f7c5ab56a"
Also we notice that the request is made to `/invoices`
## Architecture (personal note)
So we have .billing talking through an api (for the future: always check api param and look also for 500 code). I should have recalled earlier that the only subdomain acting as an api was admin. Anyway we were able to hijack the connection by observing the X-Token header.

# admin.vulntraining.co.uk/invoices
With a little backtrack I remembered that the admin subdomain offered a /invoices endpoint. Making a request with the X-Token header we can now access the api.

# content discovery, again
With ffuf, using `-recursion -recursion-depth 2 -recursion-strategy greedy`, we can recursively fuzz the api. Here are the findings:
- admin/users/{x} where x is a number. If not found it will respond with 400
- invoices/{1,2,3,4}