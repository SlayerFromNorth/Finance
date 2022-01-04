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

def tekstverdier(input):
    if input[-2:] == "kg":
        gg = re.compile("kr")
        result = re.search(gg, input)
        start = result.end() + 1
        pris = f"kr {input[start:-3]}"
        return pris, "1 kg"

    elif input[-1:] == "l":
        gg = re.compile("kr")
        result = re.search(gg, input)
        start = result.end() + 1
        pris = f"kr {input[start:-2]}"
        return pris, "1 liter"

    elif input[-3:] == "stk":
        gg = re.compile("kr")
        result = re.search(gg, input)
        start = result.end() + 1
        pris = f"kr {input[start:-4]}"
        return pris, "1 stk"
    elif input[-4:] == "vask":
        gg = re.compile("kr")
        result = re.search(gg, input)
        start = result.end() + 1
        pris = f"kr {input[start:-5]}"
        return pris, "1 vask"
    elif input[-3:] == "par":
        gg = re.compile("kr")
        result = re.search(gg, input)
        start = result.end() + 1
        pris = f"kr {input[start:-4]}"
        return pris, "1 par"
    elif input[-7:] == "tablett":
        gg = re.compile("kr")
        result = re.search(gg, input)
        start = result.end() + 1
        pris = f"kr {input[start:-8]}"
        return pris, "1 tablett"
    elif input[-9:] == "100 meter":
        gg = re.compile("kr")
        result = re.search(gg, input)
        start = result.end() + 1
        pris = f"kr {input[start:-10]}"
        return pris, "100 meter"
    elif input[-7:] == "porsjon":
        gg = re.compile("kr")
        result = re.search(gg, input)
        start = result.end() + 1
        pris = f"kr {input[start:-8]}"
        return pris, "1 porsjon"
    else:
        return False

conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_spar_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0

link = f"https://spar.no/nettbutikk/varer/"
driver = start_chrome(link) # or start_firefox()

rs = requests.get(link)
soup = BeautifulSoup(driver.page_source, features="lxml")

ss = soup.find_all("li", class_="product-categories__item product-categories__item--inactive")
fleresiderantall = [6,3,7,4,16,2,2,6,14,10,2,4,6,12,14,5,11,10]
for index, tt in enumerate(ss, start=0):
    katt = tt.find('a', href=True)
    katt = katt['href']

    print(katt)
    driver.get(f"https://spar.no/{katt}")
    try:
        for mat in range(20):  #fleresiderantall[index]
            time.sleep(1)
            click('Vis flere')
    except:
        pass



    soup1 = BeautifulSoup(driver.page_source, features="lxml")

    aa = soup1.find_all("li", class_="ws-product-list-vertical__item")

    for morro in aa:
        c = morro.find(class_="ws-product-vertical")
        d = morro.find_all("a", class_="ws-product-vertical__link")
        try:
            b = morro.find("p", class_="ws-product-vertical__price-unit")
            prisKG = b.get_text()
            prisMengde = tekstverdier(prisKG)
        except:
            f = morro.find("div", class_="ws-product-vertical__price")
            prisMengde= (f.get_text(),"1 stk")


        try:
            m = c.find_all('a', href=True)
            online = (m[0]['href'])
            linkbilde = c.find_all('img')
            linkbilde = linkbilde[0]['src']
            name = d[1].get_text()
            tid = int(time.time())
            offline = "Norge"
            supply = prisMengde[1]
            demand = prisMengde[0]
            print(ID, tid, online, offline, supply, demand, name)
            #urllib.request.urlretrieve(f"{linkbilde}", f"../Image/spar_NO/{name}.jpg")
            cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                       (ID, tid, online, offline, supply, demand, name))
            success += 1
            ID += 1
        except:
            fails += 1
print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()