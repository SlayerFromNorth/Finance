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

conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_antonsport_NO.db')
cs = conn.cursor()

cs.execute("SELECT MAX(ID) FROM deep_learning;")


ai = cs.fetchall()
ID = ai[0][0] + 1

fails = 0
success = 0


linker =["https://www.antonsport.no/klaer?limit=2000","https://www.antonsport.no/sko?limit=2000","https://www.antonsport.no/ski?limit=2000","https://www.antonsport.no/sykkel?limit=2000",
         "https://www.antonsport.no/trening?limit=2000","https://www.antonsport.no/turutstyr?limit=2000"]


for link in linker:
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    a = soup.find_all(class_="ProductModule__Container-sc-1y4g6ka-0 gQLYEM")
    for bb in a:
        katt = bb['href']
        online = f"https://www.antonsport.no/{katt}"
        name = bb.find("div", class_="ProductModule__Name-sc-1y4g6ka-3 eFPjdc")
        name = name.get_text().replace("/", "-")
        try:
            price = bb.find("div", class_="ProductPrice__Amount-sc-1cvsemb-2 VFsKQ")
            demand = price.get_text()
            demand = f"kr {demand[:-2]}"
        except:
            price = bb.find("div", class_="ProductPrice__Amount-sc-1cvsemb-2 PGVFQ")
            demand = price.get_text()
            demand = f"kr {demand}"
        tid = int(time.time())
        offline = "Norge"
        supply = "1 stk"
        linkbilde = bb.find_all('img')
        linkbilde = linkbilde[0]['src']
        print(name, online, demand, tid, offline, linkbilde, supply)
        try:
            #with open(f"../Image/antonsport_NO/{name}.png", 'wb') as f:
            #   f.write(requests.get(linkbilde).content)
            cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                      (ID, tid, online, offline, supply, demand, name))

            ID += 1
            success += 1
        except:
            fails += 1


print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()