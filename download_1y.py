#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 18:23:45 2017

@author: rhdzmota
"""

# %% Imports 

import requests
import time 
import json

# %% Initialize response datastructure 

def getDataStructure(columns):
    json_data = {}
    for col in columns: 
        json_data[col] = []
    return json_data

# %% Download raw data 

def recursiveDownload(stock_name,_limit=5):
    
    if not _limit:
        print("\t Warning: Data couldn't be downladed. Check the stockname or your internet connection.\n\n")
        return None 
    try:
        r = requests.get("https://finance.yahoo.com/quote/{}/history?p={}".format(stock_name,stock_name))
        raw_data = eval(r.text.split("HistoricalPriceStore")[-1][13:].split("isPending")[0][:-3])
    except: 
        time.sleep(2)
        print("\t Warning: Entering recursive download: {}/7".format(5-_limit))
        raw_data  = recursiveDownload(stock_name,_limit=_limit-1)
    return raw_data 
        
#eval(r.text.split("HistoricalPriceStore")[-1][13:].split("isPending")[0][:-3])

# %% Get data 

def getResponse(json_data,raw_data):
    
    for data_line in raw_data:
        for k in json_data:
            json_data[k].append(data_line.get(k))
    
    res = {}
    res["data"]    = json_data
    res["error"]   = False
    res["message"] = None 
       
    return res 
# %% 

def getData(stock_name,columns):
    
    #stock_name = "ALSEA.MX"
    #columns = ["unadjclose","date"]
    
    # get raw data
    raw_data = recursiveDownload(stock_name)
    if raw_data is None:
        res = {"error":True,"message":"Data couldn't be downloaded; maybe the stockname or something else.","data":None}
        return  json.dumps(res)
    
    # initialize datastructure for response
    json_data = getDataStructure(columns)
    
    # fill with data 
    res = getResponse(json_data,raw_data)
    
    return json.dumps(res)
    
    
# %% 
#getData("GRUMAB.MX", ["unadjclose","date"])
# %% 


# %% 