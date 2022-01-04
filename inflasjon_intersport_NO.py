from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pyautogui
import sqlite3
import urllib.request

conn = sqlite3.connect(r'C:\Users\Marius\Desktop\Prosjekter\Helper\Inflasjon\Databaser\database_intersport_NO.db')
cs = conn.cursor()
cs.execute("SELECT MAX(ID) FROM deep_learning;")
ai = cs.fetchall()

ID = ai[0][0] + 1
fails = 0
success = 0

nav = ["https://www.intersport.no/dame","https://www.intersport.no/herre","https://www.intersport.no/barn-og-junior",
       "https://www.intersport.no/vintersport","https://www.intersport.no/turutstyr","https://www.intersport.no/sportsutstyr/","https://www.intersport.no/loping-trening",
       "https://www.intersport.no/sykkel"]

driver = webdriver.Chrome(executable_path=r"../Scrape_drivers/chromedriver.exe")
for aaa in nav:
    driver.get(aaa)
    time.sleep(2)
    mer = True
    teller = 2
    while mer:
        try:
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')
            pyautogui.keyDown('pagedown')

            elem = driver.find_element_by_xpath(f'//*[@id="js-search-result-articles"]/div[{teller}]/a')
            time.sleep(2)
            elem.click()
            teller += 2
        except:
            print("hmm")
            mer = False

    soup = BeautifulSoup(driver.page_source, features="lxml")
    a = soup.find_all("div", class_="product-desc-box")
    for tt in a:

        katt = tt.find('a', href=True)
        online = katt['href']
        #linkbilde = tt.find("span", class_="product-image-container")
        #linkbilde = linkbilde.find_all('img')
        #linkbilde = linkbilde[0]['src']
        name = tt.find(class_="name-link")
        name = name.get_text().replace("/", "-")
        price = tt.find("span", class_="price")
        demand = price.get_text().strip().replace(".", " ")
        demand = f"kr {demand[:-3]}"
        tid = int(time.time())
        offline = "Norge"
        supply = "1 stk"

        print(ID, tid, online, offline, supply, demand, name)
        try:
            #urllib.request.urlretrieve(f"{linkbilde}", f"../Image/intersport_NO/{name}.png")
            cs.execute("INSERT INTO deep_learning VALUES (?, ?, ?, ?, ?, ?,?)",
                       (ID, tid, online, offline, supply, demand, name))
            ID += 1
            success += 1
        except:
            fails += 1

print(f"fails: {fails} success: {success}")
conn.commit()
cs.close()