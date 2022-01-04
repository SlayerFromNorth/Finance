import requests
import urllib.request
import sqlite3
import re
from bs4 import BeautifulSoup
import warnings
from tqdm import tqdm
import numpy as np
import time
from helium import *

conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_zalando_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0

# 247 ble problemer, trenger ikke bilder frem til hit
linker = [["https://www.zalando.no/klaer/?p=",892],
            ["https://www.zalando.no/damesko/?p=",414],
            ["https://www.zalando.no/sport/?p=",267],
            ["https://www.zalando.no/accessories/?p=",248],
            ["https://www.zalando.no/premium/?p=",157],
            ["https://www.zalando.no/herresko/?p=",119]]

driver = start_chrome("https://www.zalando.no/klaer/?p=2") # or start_firefox()
for link in tqdm(linker):
    print(link[0])


    for linkid in range(link[1]):
        driver.get(f"{link[0]}{linkid+1}")
        soup = BeautifulSoup(driver.page_source, features="lxml")

        a = soup.find_all("div", class_="_0xLoFW _78xIQ- EJ4MLB JT3_zV")
        for gat in a:

            name = gat.find("span", class_="u-6V88 ka2E9k uMhVZi FxZV-M uc9Eq5 pVrzNP ZkIJC- r9BRio qXofat EKabf7")
            name1 = gat.find(class_="u-6V88 ka2E9k uMhVZi FxZV-M z-oVg8 pVrzNP ZkIJC- r9BRio qXofat EKabf7")
            name = name.get_text().replace("/", "-")
            name = f"{name} {name1.get_text()}"
            try:
                demand = gat.find("span", class_="u-6V88 ka2E9k uMhVZi FxZV-M z-oVg8 pVrzNP cMfkVL")
                demand = f"kr {demand.get_text()[:-3]}"
            except:
                demand = gat.find("span", class_="u-6V88 ka2E9k uMhVZi dgII7d z-oVg8 _88STHx cMfkVL")
                demand = f"kr {demand.get_text()[:-3]}"
            #linkbilde = gat.find_all('img')
            #linkbilde = linkbilde[0]['src']
            tid = int(time.time())
            katt = gat.find('a', href=True)
            online = f"{katt['href']}"
            supply = "1 stk"
            offline = "Norge"

            print(ID, tid, online, offline, supply, demand, name)
            #urllib.request.urlretrieve(f"{linkbilde}", f"../Image/zalando_NO/{name}.png")
            cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                       (ID, tid, online, offline, supply, demand, name))
            ID += 1
            success += 1

        conn.commit()
print(f"fails: {fails} success: {success}")

cs.close()