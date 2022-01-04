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


conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_jackandjones_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0

linker = [["https://www.jackjones.com/no/no/jj/klaer/?sz=44&start=0", 101],
          ["https://www.jackjones.com/no/no/jj/sko/?sz=44&start=0", 3],
          ["https://www.jackjones.com/no/no/jj/tilbehoer/?sz=44&start=0", 3],
          ["https://www.jackjones.com/no/no/jj/junior/?sz=44&start=0", 15]]

driver = start_chrome("google.no") # or start_firefox()

for link in linker:
    for link_id in range(link[1]):
        linken = f"{link[0][:-1]}{link_id*44}"

        driver.get(linken)


        soup = BeautifulSoup(driver.page_source, features="lxml")

        a = soup.find_all("div", class_="isotope-grid__item isotope-grid__item--product")
        for bb in a:
            name = bb.find("a", class_="product-tile__name__link js-product-tile-link")
            name = name.get_text().strip().replace("/", "-")
            demand = bb.find("p", class_="product-tile__price")
            demand = f"kr {demand.get_text()[:-3]}"
            linkbilde = bb.find_all('img')
            linkbilde = linkbilde[0]['src'][:-6]

            tid = int(time.time())
            katt = bb.find('a', href=True)
            online = f"{katt['href']}"
            supply = "1 stk"
            offline = "Norge"
            try:
                print(ID, tid, online, offline, supply, demand, name)
                #urllib.request.urlretrieve(f"{linkbilde}", f"../Image/jackandjones_NO/{name}.png")
                cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                           (ID, tid, online, offline, supply, demand, name))
                ID += 1
                success += 1
            except:
                fails += 1

print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()