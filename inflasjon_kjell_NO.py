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

conn = sqlite3.connect('Databaser/database_kjell_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

nav = ["https://www.kjell.com/no/produkter/data?sortBy=popularity&count=40",
       "https://www.kjell.com/no/produkter/elektro-og-verktoy?sortBy=popularity&count=40",
       "https://www.kjell.com/no/produkter/hjem-fritid?sortBy=popularity&count=40",
       "https://www.kjell.com/no/produkter/kontor?sortBy=popularity&count=40",
       "https://www.kjell.com/no/produkter/lyd-og-bilde?sortBy=popularity&count=40",
       "https://www.kjell.com/no/produkter/mobilt?sortBy=popularity&count=40",
       "https://www.kjell.com/no/produkter/nettverk?sortBy=popularity&count=40",
       "https://www.kjell.com/no/produkter/smarte-hjem?sortBy=popularity&count=40"]
classkoder = [["dl eo h3 fs", "b dv a5 h9 q r al g7 h4", "b c d2 d dd de e0 e gg gh gi gj gk gl gm gn go gp gq gr gs gt",5],#
              ["dl eo he fs", "h7 cw e7 ac fi k8", "b c d2 d dd de e0 e gg gh gi gj gk gl gm gn go gp gq gr gs gt",5],#
              ["dl eo he fs", "h7 cw e7 ac fi k8", "b c d2 d dd de e0 e gg gh gi gj gk gl gm gn go gp gq gr gs gt",5],#
              ["dl eo ha fs", "b dv a5 hg q r al g7 hb", "b c d2 d dd de e0 e go gp gq gr gs gt gu gv gw gx gy gz h0 h1",4],#feil 0 inn
              ["dl eo h3 fs", "b dv a5 h4 q r al g7 h5", "b c d2 d dd de e0 e gg gh gi gj gk gl gm gn go gp gq gr gs gt",5],#
              ["dl eo h3 fs", "b dv a5 h9 q r al g7 h4", "b c d2 d dd de e0 e gg gh gi gj gk gl gm gn go gp gq gr gs gt",5],
              ["dl eo h3 fs", "b dv a5 h9 q r al g7 h4", "b c d2 d dd de e0 e gg gh gi gj gk gl gm gn go gp gq gr gs gt",5],
              ["dl eo h3 fs", "b dv a5 h9 q r al g7 h4", "b c d2 d dd de e0 e gg gh gi gj gk gl gm gn go gp gq gr gs gt",5]]
ID = ai[0][0] + 1
fails = 0
success = 0
fails_bilde = 0
driver = webdriver.Chrome(executable_path=r"../Scrape_drivers/chromedriver.exe")

for counter, link in enumerate(nav):

    driver.get(link)
    time.sleep(1)
    try:
        elem = driver.find_element_by_xpath('//*[@id="content-container"]/div[6]/div[2]/div/div/div[3]/button[2]')
        elem.click()
    except:
        pass
    for aaa in range(classkoder[counter][3]):
        pyautogui.keyDown('pagedown')
        time.sleep(0.5)

    elem = driver.find_element_by_xpath('//*[@id="content-container"]/div[4]/div[2]/div/div[2]/div[2]/button')
    elem.click()

    for ggg in range(333):
        pyautogui.keyDown('pagedown')
        time.sleep(0.7)

    soup = BeautifulSoup(driver.page_source, features="lxml")

    a = soup.find_all("div", class_=classkoder[counter][2])

    for gg in a:
        bilde_fail = False
        print(gg)
        namet = gg.find("h3", class_=classkoder[counter][0])
        name = namet.get_text().strip().replace('\n', "").replace('/', "-")
        online = gg.find('a', href=True)
        online = f"{online['href']}"
        try:
            price = gg.find("span", class_=classkoder[counter][1])
            demand = price.get_text()
        except:
            price = gg.find("span", class_="b dv a5 hj q r al g7 h3")
            demand = price.get_text()
        supply = "1 stk"
        try:
            linkbilde1 = gg.find('img')
            linkbilde = linkbilde1['src']
            linkbilde = f"{linkbilde}"
        except:
            fails_bilde += 1
            bilde_fail = True
        tid = int(time.time())
        offline = "Norge"
        print(ID, tid, online, offline, supply, demand, name)
        try:
            if bilde_fail and 1 == 0:
                try:
                    urllib.request.urlretrieve(f"https://www.kjell.com{linkbilde}", f"../Image/kjell_NO/{name}.jpg")
                except:
                    urllib.request.urlretrieve(f"https://www.kjell.com{linkbilde}", f"../Image/kjell_NO/{ID}.jpg")
            cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                       (ID, tid, online, offline, supply, demand, name))
            ID += 1
            success += 1
        except:
            fails += 1


print(fails, fails_bilde, success)
conn.commit()
cs.close()
