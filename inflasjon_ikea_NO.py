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

conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_ikea_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0

driver = start_chrome("https://www.ikea.com/no/no/cat/produkter-products/") # or start_firefox()
soup = BeautifulSoup(driver.page_source, features="lxml")
a = soup.find_all("ul", class_="vn-list--plain vn-list vn-accordion__content")
for aa in a:
    b = aa.find_all("a", class_="vn-link vn-nav__link")
    for bb in b:
        time.sleep(2)
        underlink = bb['href']+"?page=15"
        driver.get(underlink)
        soup1 = BeautifulSoup(driver.page_source, features="lxml")
        c = soup1.find_all("div", class_="range-revamp-product-compact__bottom-wrapper")

        for ss in c:
            try:
                namet = ss.find("div", class_="range-revamp-header-section__description")
                name = namet.get_text().strip().replace('\n', "").replace('/', "-")
                online = ss.find('a', href=True)
                online = f"{online['href']}"
                price = ss.find("span", class_="range-revamp-price__integer")
                price = price.get_text().replace('.', " ")
                demand = f"kr {price}"
                #linkbilde1 = ss.find('img')
                #linkbilde = linkbilde1['src']
                #linkbilde = f"{linkbilde}"
                tid = int(time.time())
                offline = "Norge"
                supply = "1 stk"

                print(ID, tid, online, offline, supply, demand, name)
            except:
                print("fail")
                fails += 1
            try:
                #urllib.request.urlretrieve(f"{linkbilde}", f"../Image/ikea_NO/{name}.jpg")
                cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                           (ID, tid, online, offline, supply, demand, name))
                ID += 1
                success += 1
            except:
                fails += 1
print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()
