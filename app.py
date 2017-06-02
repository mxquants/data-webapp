#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 21:02:44 2017

https://mxquants-datarepo.herokuapp.com
@author: rhdzmota
"""

import os
import sys
import json
import time
import requests
from flask import Flask, request, render_template


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Return index."""
    return "There's nothing to see here.", 200


@app.route('/DefaultDownload', methods=['GET'])
def defaultDownload():
    """Download from yahoo finanice."""
    from download_1y import getData
    security = (request.args.get("pwd") == "mxquants-rules")
    if not security:
        return "Looks like someone's lost, isn't it?", 200
    stock_name = request.args.get("stock_name")
    cols = request.args.get("columns")
    columns = eval(cols) if type(cols) == str else cols
    return getData(stock_name, columns), 200


@app.route('/BanxicoSeries', methods=['GET'])
def downloadBanxicoSeries():
    """Get data from banxico website."""
    from banxico_series import getJsonResponse, availableSeries
    # /BanxicoSeries?pwd=mxquants-rules&purpose=available_series&variable_name=tiie28
    # /BanxicoSeries?pwd=mxquants-rules&purpose=download_data&variable_name=tiie28
    # recursive download function

    def recursiveDownload(variable_name, n=7, debug=False):
        # if debug, just call the json response
        if debug:
            getJsonResponse(variable_name, debug)
        # return an error message if the recursive limit is reached
        if n == 0:
            return json.dumps({
                        "error": "True",
                        "message": "Data couldn't" +
                                   " be retreived for some reason."})

        # just try until the world is over (or n==0)
        try:
            raw_data = getJsonResponse(variable_name, debug)
        except:
            raw_data = recursiveDownload(variable_name, n=n-1)
        return raw_data

    # get condition
    security = (request.args.get("pwd") == "mxquants-rules")
    if not security:
        return "Looks like someone's lost, isn't it?", 200

    # identify purpose
    purpose = request.args.get("purpose")
    if purpose is None:
        return "Looks like someone's lost, isn't it?", 200
    if purpose == "available_series":
        return availableSeries(), 200
    if purpose == "download_data":
        variable_name = request.args.get("variable_name")
        return recursiveDownload(variable_name, n=7, debug=False), 200
    return "Looks like someone's lost, isn't it?", 200


@app.route('/TreasuryYieldCurve', methods=['GET'])
def getTreasuryYieldCurve():
    """Get the yield curve."""
    from treasury import getCurrentYieldCurve
    # get condition
    security = (request.args.get("pwd") == "mxquants-rules")
    if not security:
        return "Looks like someone's lost, isn't it?", 200
    return getCurrentYieldCurve(), 200
