# Login
Exploring the WebApp, there's a `/login` endpoint which performs a POST request.
There's a fishy parameter `method` sent as parameter. With ffuf we try and bruteforce it.

# method = remote
If we send `method=remote` in the POST, we get a 403 Forbidden along with an error message and the flag. The msg says that `http://znqdo26z.auth.vulnforum.co.uk/auth` returned 404.

# fuzzing
with ffuf we fuzz `http://znqdo26z.auth.vulnforum.co.uk/`
No luck with that :/

# dns bruteforcing
with dnsrecon on `znqdo26z.auth.vulnforum.co.uk`, we discovered that wildcard entries are enabled for `auth.vulnforum.co.uk`, meaning that every DNS query of form `*.auth.vulnforum.co.uk` will resolve to `vulnauth.co.uk` (being succesfull even if the subdomain doesn't infact exists).
Nevertheless, wildcards will work only for DNS entries that are not explicitly defined (i.e if there exists an entry `test.auth.___`, it will not return the wildcard entry, so hopefully it will resolve to a different IP). For this reason, we can still bruteforce with dnsrecon and filter out the default IP address returned by the wildcard entry, finding a legit subdomain.
No luck with that...but boy am I stupid.

# curl is my friend
`curl http://vulnauth.co.uk -H "Cookie: ctfchallenge = XXX` give us the 2nd flag and also a nice form to create a new user.

# create new domain
In the form we can create a new domain for vulnauth, i.e we must provide a valid domain in the form `.auth.mydomain`, an email and a password. But what domain we should use.
I tried many domain like `auth.domainX.co.uk`. At that point, it was requested to add a CNAME entry that pointed `domainX` to `vulnauth`, but I couldn't find a way to make it work.
After a while, I realized that I actually knew a domain to use: `znqdo26z.auth.vulnforum.co.uk`!
Infact the problem was that previously there wasn't such a domain to log in (404 error status).
Now we can access the `znqdo26z.auth.vulnforum.co.uk` to create new users.

# create new users
After accessing with our credentials, we can create or edit new users.
Let's create a user "testA". We need a remote UUID. What to use? If we set for example 1, when trying to login back in vulnforum, we get an error message complaining that the UUID wasn't found in db and that it couldn't found an hash...so what if we use the hash that was in the url when visiting toby profile? `/user/...` ?
If we set that hash as UUID, we log in and obtain the 3rd flag. Notice: we are logged in as toby!

# XSS
So, we can go to user forum, `change password` thread, and live a comment that the admin (bot) will check. This is clearly an example of `persistent XSS`.
If we explore the src code of the page, we see that we can input `bbcode` (we find a comment with a link to the plugin used on github). Playing around a little bit we notice that the only tag allowed is `[img]` (you can check this by trial and error or directly visiting `http://www.vulnforum.co.uk/bbcode.conf`).
In the source code on github we see that there's a regex checking that the url to the image is a valid url with `jpg|gif...` extension.

After hours spent trying to inject some js (" and <> where filtered), I gave up with the idea of injecting a script. The only thing I managed to do was to trigger requests to whatever url I wanted.

# Change password 
Lurking around the webapp I noticed something weird. If you go to settings (to check out the feature for changing the password), with my great surprise I noticed that the password was changed via a GET request with parameters password and hash. I noticed that the hash was our user identifier. So why not to change john (admin) password and get access that way??

# SSRF
The exploit was super simple: just `[img]http://www.vulnforum.co.uk/settings/password?password=password&hash=WHATEVERHASHIDHASJOHN&c=.gif[/img]`.
This triggers a request by john to change his password into password. From that we can easily login as admin and retrieve the last flag.