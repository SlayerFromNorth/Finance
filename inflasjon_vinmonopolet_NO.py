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
from helium import *

conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\inflasjon_vinmonopolet_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0

driver = start_chrome("google.no") # or start_firefox()
#browser = webdriver.Chrome(r"C:\Users\Marius\Desktop\Prosjekter\Helper\Scrape_drivers\chromedriver.exe")
for bb in tqdm(range(1191)):
    link = f"https://www.vinmonopolet.no/search?q=:relevance:visibleInSearch:true&searchType=product&currentPage={bb}"

    driver.get(f"{link}")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, features="lxml")

    a = soup.find_all("li", class_="product-item")
    for ask in a:
        try:
            name = ask.find("div", class_="product__name")
            name = name.get_text()
            online = ask.find('a', href=True)
            online = online['href']
            offline = "Norge"
            supply = ask.find("span", class_="product__amount")
            supply = supply.get_text()
            demand = ask.find("span", class_="product__price")
            demand = demand.get_text()
            #bilde = ask.find("div", class_="product-item__image")
            #linkbilde = bilde.find_all('img')
            #linkbilde = linkbilde[0]['src']
            tid = int(time.time())

            print(ID, tid, online, offline, supply, demand, name)

            #urllib.request.urlretrieve(f"{linkbilde}", f"../Image/vinmonopolet_NO/{name}.jpg")
            cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                       (ID, tid, online, offline, supply, demand, name))
            ID += 1
            success += 1
        except:
            fails += 1
print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()
