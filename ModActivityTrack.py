# -*- coding: cp1254 -*-
import requests, re
from bs4 import BeautifulSoup
from urllib import urlencode
from operator import itemgetter

user = "username"
password = "pass"

payload = {'user[username]': user, 'user[password]': password, "reme":"true"}
headers = {"X-Requested-With": "XMLHttpRequest"}
s = requests.Session()
r = s.post("https://epicmafia.com/user/login?"+urlencode(payload), headers = headers)


modlist = s.get("https://epicmafia.com/moderator")
soup = BeautifulSoup(modlist.text)
mods = soup.find(attrs={"id": "moderator_list"})
results = {}
for i in mods.find_all("div", "mod"):
    name = i.text
    idd = int(i["id"].strip("mod_"))
    url = "https://epicmafia.com/moderator/%s" % idd
    memurl = s.get(url)
    soup2 = BeautifulSoup(memurl.text)
    data = soup2.find("table")
    stuff = []
    for d in data.find_all("tr"):
        stuff.append(int(d.find_all("td")[1].text))

    total_reports, reports_last, vios, vios_last, actions, actions_last, actions_no_reason = stuff
    #result = "%s - Total: %s, Reports last week: %s" % (name, total_reports, reports_last)
    results[name] = [reports_last, total_reports]

t = sorted(results.items(), key=itemgetter(1), reverse = True)

msg = "Daily reports ranking today:\n\r\n\r\n\r"
rank = 1
for i in t:
    name, last, total = i[0], i[1][0], i[1][1]
    i = "%s. %s - Total reports: %s - Reports last week: %s" % (rank, name, total, last)
    msg += i + "\n\r\n\r\n\r"

    rank +=1

#print msg
# msg += result + "\n\r\n\r\n\r"
# POST new reply
# https://epicmafia.com/post?topic_id=@DATA&msg=@DATA
# 200 JSON [@STATUS, post_id]


a = s.get("https://epicmafia.com/topic/61712")
print a.text
token = ""

for i in BeautifulSoup(a.text).find_all("meta"):
    token += str(i)

ok=re.search('<meta name="_csrf" content="([^"]+?)"|<meta content="([^"]+?)" name="_csrf"', token)
token=ok.group(1) or ok.group(2)
post_hd = {"X-Requested-With": "XMLHttpRequest", "x-csrf-token":token}
posting = s.post( "https://epicmafia.com/post?msg=%s&topic_id=66887" % msg, headers = post_hd)

print posting.text


    
