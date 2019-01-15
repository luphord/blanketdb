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
    '''Parse url encoded form and convert numerical types'''
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

def _parse_dt(s):
    '''Parse string using custom differential date formats like "2 days"'''
    if not s:
        return ''
    s = str(s)
    if s.lower() == 'today':
        return date.today()
    elif s.lower() == 'yesterday':
        return date.today() - timedelta(days=1)
    elif s.lower().endswith('days') or s.lower().endswith('day') or s.lower().endswith('d'):
        try:
            days = int(s.split('d')[0])
        except ValueError:
            return ''
        return datetime.now() - timedelta(days=days)
    elif s.lower().endswith('hours') or s.lower().endswith('hour') or s.lower().endswith('h'):
        try:
            hours = int(s.split('h')[0])
        except ValueError:
            return ''
        return datetime.now() - timedelta(hours=hours)
    elif s.lower().endswith('min') or s.lower().endswith('m'):
        try:
            minutes = int(s.split('m')[0])
        except ValueError:
            return ''
        return datetime.now() - timedelta(minutes=minutes)
    elif s.lower().endswith('sec') or s.lower().endswith('s'):
        try:
            seconds = int(s.split('s')[0])
        except ValueError:
            return ''
        return datetime.now() - timedelta(seconds=seconds)
    return s

def _json_default(obj):
    if isinstance(obj, datetime) or isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(type(obj))

def serialize_json(data, indent=2):
    '''Serialize to json supporting dates'''
    return json.dumps(data, indent=indent, default=_json_default)

def j(obj_to_serialize=None, **kwargs):
    '''Serialize `obj_to_serialize` or keyword arguments as dict to json
       and encode to bytes'''
    if obj_to_serialize is None:
        obj_to_serialize = kwargs
    return serialize_json(obj_to_serialize).encode('utf8')