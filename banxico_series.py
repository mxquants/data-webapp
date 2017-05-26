#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 22:10:41 2017

@author: rhdzmota
"""

# %% Imports 

import os 
import wget
import json 
import pandas as pd 

# %% Reference url 

def referenceUrl():
    return r"http://www.banxico.org.mx/SieInternet/consultasieiqy?series="
# %%  Banxico Catalog

def getFromCatalog(x=None,keys=False):
    catalog = {
            "tiie28":"SF43783",
            "tiie91":"SF43878",
            "fiscal_dollar":"SF57804",
            "cetes91":"SF43939",
            "cetes28":"SF43936",
            "souvereign_cetes28":"SF45439"}
    if not keys:
        return catalog.get(x)
    return list(catalog.keys())

# %% Download file 

def downloadFile(var):
    series_code = getFromCatalog(var)
    filename = wget.download(referenceUrl()+series_code) if series_code else None
    return filename

# %% Read File 

def readFile(filename):
    with open(filename,"r") as file: 
        f = file.read()
    os.remove(filename)
    return f 

def getDataframe(file_as_string):
    try:
        tables = pd.read_html(file_as_string)
        df     = tables[-1]
        return df.iloc[4000:]
    except: 
        return None 
    

# %% Something insane

def stringFunction():
    # don't try this at home
    string_fun = """\
def thisIsInsane(var,file_contents):
    import json 
    import pandas as pd 
    
    def getFromCatalog(x=None,keys=False):
        catalog = {
                "tiie28":"SF43783",
                "tiie91":"SF43878",
                "fiscal_dollar":"SF57804",
                "cetes91":"SF43939",
                "cetes28":"SF43936",
                "souvereign_cetes28":"SF45439"}
        if not keys:
            return catalog.get(x)
        return list(catalog.keys())
    
    def getDataframe(file_as_string):
        try:
            tables = pd.read_html(file_as_string)
            df     = tables[-1]
            return df.iloc[4000:]
        except: 
            return None 
            
            
    # get main table
    df = getDataframe(file_contents)
    if df is None: 
        return json.dumps({
                "data":None,
                "error":True,
                "message":"Error at getDataframe(file_contents) probably table not found."})
    #if debug:
    #    print(df.head())  
        
    # create response 
    res = {"data":{}}
    res["data"]["timestamp"] = df.iloc[1:,0].values.tolist()
    res["data"]["values"] = df.iloc[1:,1].values.tolist()
    res["variable_name"] = getFromCatalog(var)
    res["series_name"] = getFromCatalog(var)
    
    return json.dumps(res)
"""
    return string_fun

the_script="""exec(res["fun"]);thisIsInsane(res["data"])"""
# %% 
def getJsonResponse(var,debug=False):
    
    # download file
    filename = downloadFile(var)
    if debug:
        print(filename)
    if filename is None:
        return json.dumps({
                "data":None,
                "error":True,
                "message":"Error at downloadFile(var) check the requested variable."})
    # read file 
    file_contents = readFile(filename)
    if debug:
        print(file_contents)
        
        
    # This has to change someday... 
    res =  {"data":file_contents,
            "fun":stringFunction(),
            "instr":"""eval(res["fun"])""",
            "error":"False",
            "message":"None"}
    
    return json.dumps(res) #file_contents
    
"""        
    # get main table
    df = getDataframe(file_contents)
    if df is None: 
        return json.dumps({
                "data":None,
                "error":True,
                "message":"Error at getDataframe(file_contents) probably table not found."})
    if debug:
        print(df.head())  
        
    # create response 
    res = {"data":{}}
    res["data"]["timestamp"] = df.iloc[1:,0].values.tolist()
    res["data"]["values"] = df.iloc[1:,1].values.tolist()
    res["variable_name"] = getFromCatalog(var)
    res["series_name"] = getFromCatalog(var)
    
    return json.dumps(res)
"""

# %% 

def availableSeries():
    res = {"series_names":getFromCatalog(keys=True)}
    return json.dumps(res)
    
# %% 


# %% 







































