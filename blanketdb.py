#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''A simple HTTP accessible database for IoT projects.'''

__author__ = 'luphord'
__email__ = 'luphord@protonmail.com'
__version__ = '0.1.0'

import os, json, sqlite3
from datetime import datetime, date, timedelta
import urllib.parse

def parse_form(form_s):
    d = dict()
    for k, v in urllib.parse.parse_qsl(form_s):
        try:
            d[k] = int(v)
        except ValueError:
            try:
                d[k] = float(v)
            except ValueError:
                if v.lower() == 'true':
                    d[k] = True
                elif v.lower() == 'false':
                    d[k] = False
                else:
                    d[k] = v
    return d