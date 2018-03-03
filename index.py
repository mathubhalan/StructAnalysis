# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 23:20:35 2018

@author: Mathu_Gopalan
"""

import util,helpers,time,pyautogui,re
from selenium import webdriver
import pandas as pd


def initilize(file):
    global configs,df    
    configs = helpers.ReadConfig(file)
    print(configs)
    df = pd.read_csv(configs["InputFile"]) 
    helpers.createFolders(configs) 
    return True

def gen_ScreenSnap(method=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--load-extension='+configs["ExtensionPath"])
    # Navigate to any page... well, not just *any* page...
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.get("https://www.google.com")
    time.sleep(2)
    i=0
    if (method=="wireframe"):
        v=pyautogui.locateOnScreen("findicon.PNG")
        folder_loc = configs["wfImages"]
    else : folder_loc = configs["Rawimages"]
    
    for url,b_name in zip(df["url_name"],df["brand_name"]):
        driver.get(url.strip())
        time.sleep(2)
        pg_title = driver.title
        pg_title = re.sub('[^a-zA-Z0-9-_!@#$©*.]', '',pg_title)
        pg_title = b_name+"_"+str(i)+ "_"+ pg_title
        print(pg_title)
        if (method =="wireframe"):
             #pyautogui to click on the extension
            pyautogui.click(x=v[0],y=v[1],clicks=1,interval=0.0,button="left")
            time.sleep(5)
        util.fullpage_screenshot(driver,folder_loc,pg_title)
        i+=1
    driver.close()


initilize("config.yml")
gen_ScreenSnap()
gen_ScreenSnap("wireframe")
helpers.createcanny(configs["wfImages"],configs["cannyImg"])


