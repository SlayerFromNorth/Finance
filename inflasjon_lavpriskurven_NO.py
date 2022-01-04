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

conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_lavpriskurven_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0
driver = start_chrome(f"https://www.lavpriskurven.no/categories/alle-produkter/sort-by/2/?page=1")
for page in range(15):
    driver.get(f"https://www.lavpriskurven.no/categories/alle-produkter/sort-by/2/?page={page+1}")

    soup = BeautifulSoup(driver.page_source, features="lxml")
    a = soup.find_all("div", class_="product")
    for bb in a:
        try:
            name = bb.find("a", class_="title col-md-12")
            name = name.get_text().replace("/","-")
            demand = bb.find("span", class_="special")
            demand = f"kr {demand.get_text()}"
            linkbilde = bb.find_all('img')
            linkbilde = linkbilde[0]['src']
            tid = int(time.time())
            katt = bb.find('a', href=True)
            online = f"{katt['href']}"
            supply = "1 stk"
            offline = "Norge"

        except:
            pass
        try:
            print(ID, tid, online, offline, supply, demand[:-2], name)
            #urllib.request.urlretrieve(f"https:{linkbilde}", f"../Image/lavpriskurven_NO/{name}.png")
            cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                       (ID, tid, online, offline, supply, demand[:-2], name))
            ID += 1
            success += 1
        except:
            fails += 1

print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()