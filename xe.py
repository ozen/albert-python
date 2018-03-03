# -*- coding: utf-8 -*-
from albertv0 import *
import urllib.request
from urllib.error import URLError
import re

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "XE"
__version__ = "0.0.1"
__trigger__ = "xe "
__author__ = "Yigit Ozen"


def handleQuery(query):
    if query.isTriggered:
        args = query.string.split()
        item = Item(id='python.xe', icon=":python_module", completion=query.rawString)
        if len(args) < 3:
            item.text = 'Missing arguments'
            item.subtext = 'Usage: xe <amount> <from> <to>.'
        elif len(args) > 3:
            item.text = 'Too many arguments'
            item.subtext = 'Usage: xe <amount> <from> <to>.'
        else:
            try:
                res = urllib.request.urlopen("http://www.xe.com/currencyconverter/convert/?Amount={0[0]}&From={0[1]}&To={0[2]}".format(args)).read().decode('utf-8')
                item.text = re.search(r'<span class=(.*?)uccResultAmount(.*?)>\s*(?P<amount>\d+\.\d+)\s*</span>', res).group('amount')
            except URLError as e:
                item.text = "Request Error: {0}".format(e.reason)
            except (IndexError, AttributeError) as e:
                item.text = "Could not parse the response from the server."
            except Exception as e:
                item.text = str(e)
            item.addAction(ClipAction("Copy to clipboard", item.text))
        return item
