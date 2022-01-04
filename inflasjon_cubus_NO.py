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
import pyautogui


conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_cubus_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0

linker = ["https://cubus.com/no/dame/kolleksjon/vis-alle",
          "https://cubus.com/no/herre//kolleksjon/vis-alle/",
          "https://cubus.com/no/barn/klar/vis-alle/",
          "https://cubus.com/no/baby/klar/vis-alle/",
          "https://cubus.com/no/wow/klar/vis-alle/"]

driver = start_chrome("google.no") # or start_firefox()

for link in tqdm(linker):
    print(link)
    driver.get(link)
    for ggt in range(441):
        time.sleep(0.01)
        pyautogui.keyDown('pagedown')

    soup = BeautifulSoup(driver.page_source, features="lxml")
    a = soup.find_all("div", class_="product-card -loaded -colors-on-load -hover-img")
    for tt in a:
        namet = tt.find("h2", class_="product-card__title -name")
        name = namet.get_text()
        online = tt.find("a", class_="product-card__link")
        online = online['href']
        online = f"https://www2.cubus.com/{online}"
        try:
            price = tt.find("span", class_="product-card__price-item -current")
            demand = f"kr {price.get_text()[:-2]}"
        except:
            price = tt.find("span", class_="product-card__price-item -sale")
            demand = f"kr {price.get_text()[:-2]}"
        linkbilde1 = tt.find('img')
        linkbilde = linkbilde1['src']
        tid = int(time.time())
        offline = "Norge"
        supply = "1 stk"


        try:
            print(ID, tid, online, offline, supply, demand, name)
            #urllib.request.urlretrieve(f"{linkbilde}", f"../Image/cubus_NO/{name}.png")
            cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                       (ID, tid, online, offline, supply, demand, name))
            ID += 1
            success += 1
        except:
            fails += 1
print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()