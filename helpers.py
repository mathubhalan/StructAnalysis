# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 13:43:09 2018

@author: Mathu_Gopalan
"""
import glob, cv2, yaml, os


def createcanny(inputpath,outputpath):
    print("Started to create Canny .......")
    i=0
    for imgpath in glob.glob(inputpath+"/*.PNG"):
        base = os.path.splitext(os.path.basename(imgpath))[0]
        img = cv2.imread(imgpath)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,150,apertureSize = 3)
        cv2.imwrite(outputpath +"/"+ base +'_edg.jpg',edges)
        i+=1
    print ("Canny Images completed in folder {}".format(outputpath))
    return True

def ReadConfig(config_file):    
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
 
def createFolders(fol_loc):
    del fol_loc['InputFile']
    for k,v in fol_loc.items():
        if not os.path.exists(v):
            os.makedirs(v)
            print("Folder Created {:}".format(v))
    
               
    
        
    
                
