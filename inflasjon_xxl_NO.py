import requests
import urllib.request
import sqlite3
import re
from bs4 import BeautifulSoup
import warnings
from tqdm import tqdm
import numpy as np
import time
import pyautogui
from helium import *
from selenium import webdriver


driver = webdriver.Chrome(executable_path=r"../Scrape_drivers/chromedriver.exe")


conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_xxl_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0

linken = f"https://www.xxl.no/vintersport/langrenn/c/240200"

driver.get(linken)

soup = BeautifulSoup(driver.page_source, features="lxml")
a = soup.find_all(class_="menu__submenu-three-show-all")
print(a)
for c in a:
    try:
        link = (c['href'])
        linken = f"https://www.xxl.no{link}?pages=200"

        driver.get(linken)
        driver.get(linken)
        time.sleep(170)
        for gg in range(55):
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')
            time.sleep(0.5)
        soup1 = BeautifulSoup(driver.page_source, features="lxml")

        b = soup1.find_all("div", class_="product-list__info-wrapper")
        c = soup1.find_all("div", class_="category-list__product-list test-category__product-list")

        underlink = c[0].find_all('a', href=True)

        print(len(b), len(underlink))
        for count, d in enumerate(b):
            online = underlink[count]['href']
            online = f"https://www.xxl.no{online}"
            try:
                price = d.find("p", class_="product-list__price product-list__price--discount test-category__product-price")
                demand = f"kr {price.get_text()[:-2]}"
            except:
                price = d.find("p", class_="product-list__price test-category__product-price")
                demand = f"kr {price.get_text()[:-2]}"

            name = d.find("p", class_="product-list__brand test-category-filtering__product-brand")
            name1 = d.find("h2")
            name = name.get_text().replace("/", "-")
            name = f"{name} {name1.get_text()}"
            # linkbilde = d.find_all('img')
            # linkbilde = linkbilde[0]['src']
            # linkbilde = f"https://www.xxl.no{linkbilde}"
            supply = "1 stk"
            offline = "Norge"
            tid = int(time.time())

            print(ID, tid, online, offline, supply, demand, name)
            try:
                #urllib.request.urlretrieve(f"{linkbilde}", f"../Image/xxl_NO/{name}.png")
                cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                           (ID, tid, online, offline, supply, demand, name))
                ID += 1
                success += 1
            except:
                fails += 1
    except:
        pass
print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()