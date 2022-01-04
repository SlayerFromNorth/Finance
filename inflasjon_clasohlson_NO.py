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

conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_clasohlson_NO.db')
cs = conn.cursor()

cs.execute("SELECT MAX(ID) FROM deep_learning;")


ai = cs.fetchall()
ID = ai[0][0] + 1

fails = 0
success = 0

driver = start_chrome("google")  # or start_firefox()
r = requests.get("https://www.clasohlson.com/no/Hjem/c/1035")
#driver = start_chrome("google.no") # or start_firefox()
soup = BeautifulSoup(r.text, 'html.parser')

a = soup.find_all("ul", class_="thirdLevel-1")

for gg in a:
    underlink = gg.find('a', href=True)
    pages = 1
    for tt in range(100):
        link = f"https://www.clasohlson.com{underlink['href']}?page={tt+ pages}"
        driver.get(link)
        time.sleep(1)
        soup1 = BeautifulSoup(driver.page_source, features="lxml")
        b = soup1.find_all("div", class_="product-card__mid")
        if (len(b) < 1):
            break
        for ss in b:
            namet = ss.find("a", class_="name")
            name = namet.get_text().strip().replace('\n', "").replace('/', "-")
            online = ss.find('a', href=True)
            online = f"{online['href']}"
            price = ss.find("div", class_="price")
            splittet = price.get_text().strip()
            demand = f"kr {splittet}"

            supply = "1 stk"
            tak = ss.find("a", class_="thumb")
            #linkbilde1 = tak.find('img')
            #linkbilde = linkbilde1['data-src']
            #linkbilde = f"{linkbilde}"
            tid = int(time.time())
            offline = "Norge"

            print(ID, tid, online, offline, supply, demand, name) #linkbilde
            try:

                #urllib.request.urlretrieve(f"{linkbilde}", f"../Image/clasohlson_NO/{name}.jpg")
                cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                           (ID, tid, online, offline, supply, demand, name))
                ID += 1
                success += 1
            except:
                print("fail")
                fails += 1
print(f'fails:{fails}, success: {success}')
conn.commit()
cs.close()