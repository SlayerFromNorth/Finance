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

conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_obs_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0

nav = [["https://coop.no/sortiment/obs-sortiment/sport-og-fritid",'//*[@id="content-container"]/main/div[2]/div[1]/div[2]/span/button'],
       ["https://coop.no/sortiment/obs-sortiment/kjaledyr",'//*[@id="content-container"]/main/div[2]/div[1]/div[2]/span/button'],
       ["https://coop.no/sortiment/obs-sortiment/kjokkenutstyr-og-borddekking",'//*[@id="content-container"]/main/div[2]/div[2]/div[2]/span/button'],
       ["https://coop.no/sortiment/obs-sortiment/elektronikk",'//*[@id="content-container"]/main/div[2]/div[2]/div[2]/span/button'],
       ["https://coop.no/sortiment/obs-sortiment/fest-og-hoytid",'//*[@id="content-container"]/main/div[2]/div[2]/div[2]/span/button'],
       ["https://coop.no/sortiment/obs-sortiment/leker",'//*[@id="content-container"]/main/div[2]/div[2]/div[2]/span/button'],
       ["https://coop.no/sortiment/obs-sortiment/hjem-og-interior",'//*[@id="content-container"]/main/div[2]/div[2]/div[2]/span/button']]


driver = webdriver.Chrome(executable_path=r"../Scrape_drivers/chromedriver.exe")
for ss in nav[1:2]:
    driver.get(ss[0])

    mer = False
    time.sleep(2)
    while mer:

        try:
              pyautogui.keyDown('pagedown')
              pyautogui.keyDown('pagedown')
              pyautogui.keyDown('pagedown')
              pyautogui.keyDown('pagedown')
              pyautogui.keyDown('pagedown')

              elem = driver.find_element_by_xpath(ss[1])
              print(elem)
              time.sleep(2)
              elem.click()
        except:
              print("hmm")
              mer = False
    for ggg in range(1):
        pyautogui.keyDown('pagedown')
        pyautogui.keyDown('pagedown')
        pyautogui.keyDown('pagedown')
        pyautogui.keyDown('pagedown')

        time.sleep(2)


    soup1 = BeautifulSoup(driver.page_source, features="lxml")
    a = soup1.find_all("div", class_="product-card style_productCard__CjHBG style_grid__3mJVA style_gridCard__Ne8XP")
    print(a)
    for GG in a:
        name = GG.find("span", class_="style_name__203YW")
        name = name.get_text()
        try:
            demand = GG.find("span", class_="style_productCardPrice__1ZTJ9")
            demand = f"kr {demand.get_text()}"

        except:
            try:
                demand = GG.find("span", class_="style_productCardPrice__1ZTJ9 style_memberPrice__3GvJy")
                demand = f"kr {demand.get_text()}"
            except:
                demand = GG.find("span", class_="style_productCardPrice__1ZTJ9 style_campaignPrice__2Rw1r")
                demand = f"kr {demand.get_text()}"

        #linkbilde = GG.find("div", class_="image")
        #linkbilde = linkbilde.find_all('img')
        #linkbilde = linkbilde[0]['src']
        tid = int(time.time())
        katt = GG.find('a', href=True)
        online = f"https://coop.no{katt['href']}"
        supply = "1 stk"
        offline = "Norge"
        print(ID, tid, online, offline, supply, demand, name)
        try:
            #urllib.request.urlretrieve(f"https://coop.no{linkbilde}", f"../Image/obs_NO/{name[0:7]}.jpg")
            cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                       (ID, tid, online, offline, supply, demand, name))
            ID += 1
            success += 1
        except:
            fails += 1
print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()