#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 16:42:09 2017
Simple neural networks using tensorflow

@author: rhdzmota
"""
# Imports
import requests
import pandas as pd
import json

def getCurrentYieldCurve():
    """Return the current yield curve."""
    def getHTMLTreasury():
        """Download data from treasury webpage."""
        _url = "https://www.treasury.gov/resource-center/data-chart-center/" +\
               "interest-rates/Pages/TextView.aspx?data=yield"
        r = requests.get(_url)
        return r.text

    def getHTMLTable(html_response):
        """Extract (if possible) html table form response."""
        _table = ("""<table class="t-chart" """ +
                  html_response.split(""" class="t-chart" """)[-1]).split(
                  "</table>")[0]+"</table>"
        return _table

    def html2Df(_table):
        """Get a pandas dataframe from an html table."""
        return pd.read_html(_table)[0]
    try:
        _html = getHTMLTreasury()
        _table = getHTMLTable(_html)
        df = html2Df(_table).T
        df.columns = ["period", "rate"]
        return json.dumps({"data": df.iloc[1:],
                           "reference_date": df.iloc[0, 1],
                           "error": "False", "message": "None"})
    except:
        return json.dumps({"data": "None",
                           "reference_date": "None",
                           "error": "True", "message": "Okay, this is weird." +
                           " May be the internet connection or getHTMLTable()."
                           })
