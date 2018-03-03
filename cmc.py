# -*- coding: utf-8 -*-
from albertv0 import *
import urllib.request
import json
import re

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "CoinMarketCap"
__version__ = "0.0.1"
__trigger__ = "cmc "
__author__ = "Yigit Ozen"


def get_rate(from_cur, to_cur):
    with urllib.request.urlopen('https://api.coinmarketcap.com/v1/ticker/?convert={0}'.format(to_cur)) as response:
        data = response.read().decode("utf-8")
        data_dict = json.loads(data)

        for cur in data_dict:
            if cur['symbol'].lower() == from_cur:
                rate = cur['price_{0}'.format(to_cur)]
                return float(rate)
        
    return None


def handleQuery(query):
    if query.isTriggered:
        args = query.string.split()
        item = Item(id='python.cmc', icon=":python_module", completion=query.rawString)
        if len(args) < 3:
            item.text = 'Missing arguments'
            item.subtext = 'Usage: cmc <amount> <from> <to>.'
        elif len(args) > 3:
            item.text = 'Too many arguments'
            item.subtext = 'Usage: cmc <amount> <from> <to>.'
        else:
            amount = int(args[0])
            from_cur = args[1].lower()
            to_cur = args[2].lower()

            rate = get_rate(from_cur, to_cur)

            if rate is None:
                rate = get_rate(to_cur, from_cur)

                if rate is None:
                    item.text = 'Could not find the answer'
                else:
                    item.text = str(amount/rate)
            else:
                item.text = str(amount*rate)
            item.addAction(ClipAction("Copy to clipboard", item.text))
        return item
