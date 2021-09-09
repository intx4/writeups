# Domain discovery
` dnsrecon -d vulntraining.co.uk -D /home/intx/ctf/ctfchallenge/subdomains.txt -n 8.8.8.8 -t brt`

Sub-domains found:
- billing
- admin
- www

With crt.sh enumaration we find also `c867fc3a.vulntraining.co.uk` which gives the first flag.