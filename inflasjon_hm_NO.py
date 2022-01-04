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


conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_hm_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0
# Trenger VPN!!!!! Blir blokkert
linker =["https://www2.hm.com/no_no/home/produkter/se-alle.html?sort=stock&image-size=small&image=stillLife&offset=0&page-size=2125",
         "https://www2.hm.com/no_no/dame/produkter/se-alle.html?sort=stock&image-size=small&image=model&offset=0&page-size=8747",
         "https://www2.hm.com/no_no/herre/produkter/se-alle.html?sort=stock&image-size=small&image=model&offset=0&page-size=2177",
         "https://www2.hm.com/no_no/divided/shop-by-product/view-all.html?sort=stock&image-size=small&image=model&offset=0&page-size=2348",
         "https://www2.hm.com/no_no/barn/shop-by-product/view-all.html?sort=stock&image-size=small&image=stillLife&offset=0&page-size=7118"]

driver = start_chrome("https://www2.hm.com/no_no/barn/produkter/baby-jente-68-92.html?product-type=kids_babygirl_all&sort=stock&image-size=small&image=stillLife&offset=0&page-size=12") # or start_firefox()

for link in tqdm(linker):
    print(link)
    time.sleep(15)
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, features="lxml")
    a = soup.find_all("li", class_="product-item")
    for tt in a:
        try:
            namet = tt.find("a", class_="link")
            name = namet.get_text()
            online = namet['href']
            online = f"https://www2.hm.com/{online}"
            price = tt.find("span", class_="price regular")
            demand = f"kr {price.get_text()[:-4]}"
            #linkbilde1 = tt.find('img')
            #linkbilde = linkbilde1['src']
            #linkbilde = f"http:{linkbilde}"
            tid = int(time.time())
            offline = "Norge"
            supply = "1 stk"
        except:
            pass


        try:
            #driver.get(online)
            #soup1 = BeautifulSoup(driver.page_source, features="lxml")
            #gg = soup1.find("div", class_="product-detail-main-image-container")

            #linkbilde2 = gg.find('img')
            #linkbilde3 = linkbilde2['src']
            #linkbilde4 = f"http:{linkbilde3}"

            #urllib.request.urlretrieve(f"{linkbilde4}", f"../Image/hm_NO/{name}.png")
            #with open(f"Image/hm_NO/{name}.png", 'wb') as f:
            #   f.write(requests.get(linkbilde).content)
            print(ID, tid, online, offline, supply, demand, name)
            cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                       (ID, tid, online, offline, supply, demand, name))
            ID += 1
            success += 1
        except:
            fails += 1
print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()