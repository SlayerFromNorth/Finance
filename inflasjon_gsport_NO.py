from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pyautogui
import sqlite3
import urllib.request
# --------------- LAGT NED -------------------
conn = sqlite3.connect('Databaser/database_gsport_NO.db')
cs = conn.cursor()

ID = 0
fails = 0
success = 0

nav = ["https://www.gsport.no/dame","https://www.gsport.no/herre","https://www.gsport.no/barn-og-junior",
       "https://www.gsport.no/turutstyr","https://www.gsport.no/sport-ballspill","https://www.gsport.no/loping-trening"]

driver = webdriver.Chrome(executable_path=r"../Scrape_drivers/chromedriver.exe")
time.sleep(4)
for aaa in nav:
    driver.get(aaa)
    time.sleep(2)

    mer = True
    while mer:

        try:
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pageup')


            time.sleep(5.5)
            elem = driver.find_element_by_class_name("amscroll-load-button")
            print(elem)

            elem.click()
        except:
            mer = False

    soup = BeautifulSoup(driver.page_source, features="lxml")
    a = soup.find_all("div", class_="product-item-info")
    for tt in a:

        katt = tt.find('a', href=True)
        online = katt['href']
        linkbilde = tt.find("span", class_="product-image-container")
        linkbilde = linkbilde.find_all('img')
        linkbilde = linkbilde[0]['src']
        name = tt.find(class_="product name product-item-name")
        name = name.get_text().replace("/","-")
        price = tt.find("a", class_="product-item-price")
        demand = price.get_text().strip()
        demand = f"kr {demand[:-3]}"
        tid = int(time.time())
        offline = "Norge"
        supply = "1 stk"

        print(ID, tid, online, offline, supply, demand, name)
        try:
            #urllib.request.urlretrieve(f"{linkbilde}", f"../Image/gsport_NO/{name}.png")
            #cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
            #           (ID, tid, online, offline, supply, demand, name))
            ID += 1
            success += 1
        except:
            fails += 1

print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()