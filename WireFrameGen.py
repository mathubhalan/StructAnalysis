# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 13:31:01 2018
To Gen a Wireframe from a given web page
@author: Mathu_Gopalan
#######################################
Step 1: Read the URL from CSV
Step 2: OPen the Chrome Browser 
Step 3: Navigate to the URL 
Step 4: convert the page as wireframe, by calling the extenstion
"""
import os,yaml, time, util, pyautogui
from selenium import webdriver
from urllib.parse import urlparse
from PIL import Image
import pandas as pd


def readconfig(config):
    #code to read the config section #
    global BaseFolder, InputFile,SnapFolder,df,fixedheader    
    with open(config,'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        #print (cfg)
    for section in cfg:
        BaseFolder = cfg["Path"]["BaseFolder"]
        InputFile = cfg["Path"]["InputFile"]
        SnapFolder = cfg["Path"]["SnapFolder"]
        fixedheader = cfg["FixedHeader"]
    df = pd.read_csv(InputFile)    
    print("Config completed")
    create_basefolder(BaseFolder,SnapFolder,InputFile)
 
def create_basefolder(BaseFolder,SnapFolder,InputFile):
    print ("creating folders basefolder : {}, snap folder{}..".format(BaseFolder,SnapFolder))
    if not os.path.exists(BaseFolder):
        os.makedirs(BaseFolder)
    #create snap folder    
    if not os.path.exists(SnapFolder):
        os.makedirs(SnapFolder)          
    print("folder creation completed")
    
#gen the raw images
def gen_PNG():
    options = webdriver.ChromeOptions()
    #user local machine path to wireframify chrom extn
    cx = "C:/Users/mathu_gopalan/AppData/Local/Google/Chrome/User Data/Default/Extensions/denkephjglddepmhdlaaigjionglkdbb/1.0.1_0/"
    # Note that `chrome-extension` is the path to the unpackaged extension.
    options.add_argument('--load-extension='+cx)
    # Navigate to any page... well, not just *any* page...
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    time.sleep(2)
    i=0
    for url in df["URLs_name"]:
        driver.get(url.strip())
        time.sleep(2)
        util.fullpage_screenshot(driver,SnapFolder,str(i))
        i+=1
    
        

def gen_Wireframe():
    options = webdriver.ChromeOptions()
    cx = "C:/Users/mathu_gopalan/AppData/Local/Google/Chrome/User Data/Default/Extensions/denkephjglddepmhdlaaigjionglkdbb/1.0.1_0/"
    # Note that `chrome-extension` is the path to the unpackaged extension.
    options.add_argument('--load-extension='+cx)
    # Navigate to any page... well, not just *any* page...
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.get("https://www.google.com")    
    time.sleep(2)
    v=pyautogui.locateOnScreen("findicon.PNG")
    i=0
    for url in df["URLs_name"]:
        driver.get(url.strip())
        time.sleep(2)      
        #pyautogui to click on the extension
        pyautogui.click(x=v[0],y=v[1],clicks=1,interval=0.0,button="left")
        time.sleep(5)
        util.fullpage_screenshot(driver,SnapFolder,str(i))
        i+=1
            
def main():
    readconfig('config.yml')
    gen_PNG()
    gen_Wireframe()
    


    
