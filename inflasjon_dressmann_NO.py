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


conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_dressmann_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0
driver = start_chrome("https://dressmann.com/no/nettbutikk-s-9xl/dressmann/blazers/") # or start_firefox()
soup = BeautifulSoup(driver.page_source, features="lxml")

b = soup.find_all("a", class_="sidebar-nav__link")
for sss in b[3:-4]:
    onlinelink = sss['href']
    print(onlinelink)
    driver.get(f"https://dressmann.com/{onlinelink}")
    for ttt in range(44):
        time.sleep(0.1)
        pyautogui.keyDown('pagedown')

    soup1 = BeautifulSoup(driver.page_source, features="lxml")
    riktige = soup1.find("ul", class_="product-list")
    a = riktige.find_all("div", class_="product-card -loaded -colors-on-hover -colors-on-load -hover-img")

    for tt in a:
        try:
            namet = tt.find("h2", class_="product-card__title -name")
            name = namet.get_text()
            online = tt.find("a", class_="product-card__link")
            online = f"https://www2.dressmann.com{online['href']}"
            price = tt.find("span", class_="product-card__price-item -current")
            demand = f"kr {price.get_text()[:-2]}"
            linkbilde1 = tt.find('img')
            linkbilde = linkbilde1['src']
            linkbilde = f"{linkbilde}"
            tid = int(time.time())
            offline = "Norge"
            supply = "1 stk"
        except:
            fails += 1
            print("feil1")
        try:
            print(ID, tid, online, offline, supply, demand, name)
            #urllib.request.urlretrieve(f"{linkbilde}", f"../Image/dressmann_NO/{name}.png")
            cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                       (ID, tid, online, offline, supply, demand, name))
            ID += 1
            success += 1
        except:
            fails += 1
            print("feil")

print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()