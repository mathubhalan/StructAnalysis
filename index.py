# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 23:20:35 2018

@author: Mathu_Gopalan
"""

import helpers
import pandas as pd


def initilize(file):
    global configs,df    
    configs = helpers.readconfig(file)
    print(configs)
    df = pd.read_csv(configs["InputFile"]) 
    helpers.createfolders(configs) 
    return True



initilize("config.yml")
helpers.gen_screensnap(df, configs)
helpers.gen_screensnap(df, configs,"wireframe")
helpers.createcanny(configs["wfImages"],configs["cannyImg"])


