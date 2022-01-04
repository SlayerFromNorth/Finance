import requests
import urllib.request
import sqlite3
import re
from bs4 import BeautifulSoup
import warnings
from tqdm import tqdm
import numpy as np
import time
from selenium import webdriver
import pyautogui

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
    else:
        return False

conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_meny_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0

link = f"https://meny.no/varer"
driver = webdriver.Chrome(executable_path=r"../Scrape_drivers/chromedriver.exe")

driver.get(link)
soup = BeautifulSoup(driver.page_source, features="lxml")

ss = soup.find_all("li", class_="cw-categories__item only-small-categories cw-categories__item--inactive")

for tt in ss:
    katt = tt.find('a', href=True)
    katt = katt['href']

    driver.get(f"https://meny.no/{katt}")

    mer = True
    while mer:
        try:
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')

            elem = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/main/div/div/div[3]/div/div[2]/button')
            elem.click()
            time.sleep(2)
        except:
            mer = False


    soup1 = BeautifulSoup(driver.page_source, features="lxml")

    aa = soup1.find_all("div", class_="ws-product-vertical__details")
    for morro in aa:
        c = morro.find(class_="cw-product__link")
        d = morro.find("div", class_="ws-product-vertical__link")
        try:
            b = morro.find("p", class_="ws-product-vertical__price-unit")
            prisKG = b.get_text()
            prisMengde = tekstverdier(prisKG)
        except:
            pass

        try:
            prisen_kroner = morro.find("div", class_="ws-product-vertical__price").get_text()
            prisMengde = (f"{prisen_kroner}", "1 stk")
            online = "-"
            #linkbilde = c.find_all('img')
            #linkbilde = linkbilde[0]['src']
            name = d.get_text()
            tid = int(time.time())
            offline = "Norge"
            supply = prisMengde[1]
            demand = prisMengde[0]
            print(ID, tid, online, offline, supply, demand, name)
            #urllib.request.urlretrieve(f"{linkbilde}", f"../Image/meny_NO/{name}.jpg")
            cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                       (ID, tid, online, offline, supply, demand, name))
            success += 1
            ID += 1
        except:
            fails += 1
print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()
