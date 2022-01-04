import requests
import urllib.request
import sqlite3
import re
from bs4 import BeautifulSoup
import warnings
from tqdm import tqdm
import numpy as np
import time

def find_enhet(inn):
    if inn[-2:] == "kg":
        return[inn[:-7], "1 kg"]
    elif inn[-1:] == "l":
        return[inn[:-6], "1 liter"]
    elif inn[-3:] == "stk":
        return[inn[:-8], "1 stk"]

conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\inflasjon_kolonial_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0


r = requests.get("https://kolonial.no/kategorier/20-frukt-og-gront/")
soup = BeautifulSoup(r.text, 'html.parser')
a = soup.find_all("li", class_="parent-category")
linker_hoved = []
for c in a:
    linker = []
    for b in c.find_all('a', href=True):
        linker.append(b['href'])

    linker_hoved.append(linker[0])

#for a in linker_hoved:
#    print(f"https://kolonial.no{a}")
for linkene_hoved in linker_hoved[2:]:
    rs = requests.get(f"https://kolonial.no{linkene_hoved}")
    soup1 = BeautifulSoup(rs.text, 'html.parser')

    f = soup1.find_all("li", class_="child-category")
    linker_under = []
    for c in f:
        linker = []
        for b in c.find_all('a', href=True):
            linker.append(b['href'])
        linker_under.append(linker[0])
    for a in linker_under:
        print(f"https://kolonial.no{a}")
    #
    for linkene_under in linker_under:
        page = 1
        while(page):
            rsa = requests.get(f"https://kolonial.no{linkene_under}?page={page}")
            soup2 = BeautifulSoup(rsa.text, 'html.parser')

            atta = soup2.find_all("div", class_="product-list-item")

            for batwoman in atta:
                name = batwoman.find("div", class_="name-main wrap-two-lines")
                texttitle = name.get_text().replace("/", " ")
                price = batwoman.find_all("p", class_="unit-price")
                etterspørsel_tilbud = find_enhet(price[0].get_text().strip()) #list
                gatta = batwoman.find('a', href=True)
                online = (f"https://kolonial.no{gatta['href']}")
                offline = "Norge"
                linkbilde = batwoman.find_all('img')
                linkbilde = linkbilde[0]['src']
                tid = int(time.time())
                try:
                    print(ID, tid, online, offline, etterspørsel_tilbud[1], etterspørsel_tilbud[0], texttitle)
                    # urllib.request.urlretrieve(f"{linkbilde}", f"../Image/kolonial_no/{texttitle}.jpg")
                    cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                               (ID, tid, online, offline, etterspørsel_tilbud[1], etterspørsel_tilbud[0], texttitle))
                except:
                    fails += 1
                ID += 1
                success += 1
            try:
                next = soup2.find("ul", class_="pagination")
                matta = next.find_all('a', href=True)
                if page+1 < len(matta):
                    page += 1
                else:
                    page = False
            except:
                page = False
                print("feil")
print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()
