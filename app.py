#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 21:02:44 2017

https://mxquants-datarepo.herokuapp.com
@author: rhdzmota
"""

# %% Imports 

import os
import sys
import json
import time 
import requests
from flask import Flask, request, render_template

# %% Declare App 

app = Flask(__name__)


# %% Index 

@app.route('/', methods=['GET'])
def index():    
    return "There's nothing to see here.",200

# %% 

@app.route('/DefaultDownload', methods=['GET'])
def defaultDownload():
    from download_1y import getData
    
    
    # get condition 
    security = (request.args.get("pwd") == "mxquants-rules") 
    if not security: 
        return "Looks like someone's lost, isn't it?",200
    
    # get relevant vars
    stock_name = request.args.get("stock_name")
    columns    = eval(request.args.get("columns"))
    
    return getData(stock_name,columns),200

# %% 


# %% 


# %% 


# %% 


# %% 


# %% 


# %% 


# %% 


# %% 


# %% 


# %% 