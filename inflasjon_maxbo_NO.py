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
from selenium import webdriver
import pyautogui


conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_maxbo_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0

nav = ["https://www.maxbo.no/gulv/","https://www.maxbo.no/maling-og-tapet/","https://www.maxbo.no/verktoy-redskap-og-maskiner/",
       "https://www.maxbo.no/kjokken-og-bad/","https://www.maxbo.no/ovn-peis-og-oppvarming/","https://www.maxbo.no/interior/","https://www.maxbo.no/dor-og-vindu/",
       "https://www.maxbo.no/hage-og-uteomrade/","https://www.maxbo.no/garderobe-og-oppbevaring/","https://www.maxbo.no/belysning-og-elektromateriell/",
       "https://www.maxbo.no/arbeidsklaer-og-sikkerhet/"]


driver = webdriver.Chrome(executable_path=r"../Scrape_drivers/chromedriver.exe")
for dd in nav:
    driver.get(dd)
    mer = True
    while mer:
           try:
                  pyautogui.keyDown('pagedown')
                  pyautogui.keyDown('pagedown')
                  pyautogui.keyDown('pagedown')
                  pyautogui.keyDown('pagedown')
                  pyautogui.keyDown('pagedown')

                  elem = driver.find_element_by_xpath('//*[@id="mainContent"]/main/div[1]/div[2]/a/div/button')
                  elem.click()
                  time.sleep(2)
           except:
                  mer = False
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, features="lxml")
    b = soup.find_all("div", class_="product__container")


    for kk in b:
        try:
            namet = kk.find("h3", class_="product__title")
            name = namet.get_text().strip().replace('\n', "").replace('/', "-")
            online = kk.find('a', href=True)
            online = f"{online['href']}"
            price = kk.find("span", class_="product__price-value")
            splittet = price.get_text().split(",-")
            demand = f"kr {splittet[0]}"

            supply = "1 stk"
            # linkbilde1 = kk.find('img')
            # linkbilde = linkbilde1['src']
            # linkbilde = f"{linkbilde}"
            tid = int(time.time())
            offline = "Norge"

            print(ID, tid, online, offline, supply, demand, name)
            # urllib.request.urlretrieve(f"https://www.maxbo.no{linkbilde}", f"../Image/maxbo_NO/{name}.jpg")
            cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                       (ID, tid, online, offline, supply, demand, name))

            ID += 1
            success += 1
        except:
            fails += 1

print(f'fails:{fails}, success: {success}')
conn.commit()
cs.close()
