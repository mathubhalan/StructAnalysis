# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 13:43:09 2018

@author: Mathu_Gopalan
"""
import glob, cv2, yaml, os, re, time,pyautogui, util
from selenium import webdriver


def createcanny(inputpath,outputpath):
    print("Started to create Canny .......")
    i=0
    for imgpath in glob.glob(inputpath+"/*.PNG"):
        base = os.path.splitext(os.path.basename(imgpath))[0]
        img = cv2.imread(imgpath)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,150,apertureSize = 3)
        op = outputpath +"/"+ base +'_edg.jpg'
        cv2.imwrite(op,edges)
        print ("Canny created: {}".format(op))
        i+=1
    print ("Canny Images completed in folder {}".format(outputpath))
    return True

def readconfig(config_file):    
    with open(config_file,'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    for section in cfg:
        InputFile = cfg["Path"]["InputFile"]
        SnapFolder = cfg["Path"]["SnapFolder"]
        fixedheader = cfg["FixedHeader"]
        ExtensionPath = cfg["ExtensionPath"]
    Rawimages = SnapFolder + "/RawImages"
    wfImages = SnapFolder + "/wireFrames"
    cannyImg = SnapFolder + "/Canny"
    clusterpath = SnapFolder + "/clusters"
    config = {"InputFile" : InputFile,
              "SnapFolder" : SnapFolder,
              "fixedheader": fixedheader,
              "Rawimages" : Rawimages,
              "wfImages" : wfImages,
              "cannyImg" : cannyImg,
              "clusterpath" :clusterpath,
              "ExtensionPath" : ExtensionPath}
    print("Configurations completed")          
    return config
 
def createfolders(fol_loc):
    del fol_loc['InputFile']
    for k,v in fol_loc.items():
        if not os.path.exists(v):
            os.makedirs(v)
            print("Folder Created {:}".format(v))

def slugify(title):
    name = title.replace(' ', '-').lower()
    #remove `other` characters
    name = re.sub('[^a-zA-Z0-9_-]','', name)
    #nomalize dashes
    name = re.sub('-+', '-', name)
    print(name)
    return name     

def gen_screensnap(df,configs,method=None):
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
    
    for url,b_name in zip(df["urls_name"],df["brand_name"]):
        driver.get(url.strip())
        time.sleep(2)
        pg_title = driver.title
        pg_title = slugify(pg_title)
        #pg_title = re.sub('[^a-zA-Z0-9-_!@#©|?|$|.|!*.]', '',pg_title)
        pg_title = b_name+"_"+str(i)+ "_"+ pg_title
        if len(pg_title)>240:
            pg_title = pg_title[0:239]
        print(pg_title)
        if (method =="wireframe"):
             #pyautogui to click on the extension
            pyautogui.click(x=v[0],y=v[1],clicks=1,interval=0.0,button="left")
            time.sleep(5)
        util.fullpage_screenshot(driver,folder_loc,pg_title)
        i+=1
    driver.close()
