#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for helper functions"""


import unittest
import json

from datetime import datetime, date, timedelta
from blanketdb import _parse_form, _parse_dt, _serialize_json, _j


def is_close(dt1, dt2, max_diff_sec=10):
    return abs(dt1.timestamp() - dt2.timestamp()) < max_diff_sec


class TestHelperFunctions(unittest.TestCase):
    """Tests for helper functions"""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_parse_form(self):
        '''Test function for parsing and type converting forms'''
        self.assertEqual(dict(a='b'), _parse_form('a=b'))
        self.assertEqual(dict(a='b', c='d'), _parse_form('a=b&c=d'))
        self.assertEqual(dict(a=1), _parse_form('a=1'))
        self.assertEqual(1.1, _parse_form('a=1.1')['a'])
        self.assertEqual(float, type(_parse_form('a=1.0')['a']))
        self.assertEqual(dict(a=True), _parse_form('a=true'))
        self.assertEqual(dict(a=False), _parse_form('a=false'))

    def test_parse_date(self):
        '''Test function for customized date parsing'''
        self.assertEqual('', _parse_dt(''))
        # this function only parses dates in custom format
        self.assertEqual('2025-02-03', _parse_dt('2025-02-03'))
        self.assertEqual('', _parse_dt(None))
        self.assertEqual(date.today(), _parse_dt('today'))
        self.assertEqual(date.today() - timedelta(days=1),
                         _parse_dt('yesterday'))
        # days
        self.assertTrue(is_close(datetime.now() - timedelta(days=2),
                        _parse_dt('2d')))
        self.assertTrue(is_close(datetime.now() - timedelta(days=2),
                        _parse_dt('2days')))
        self.assertTrue(is_close(datetime.now() - timedelta(days=2),
                        _parse_dt('2 days')))
        self.assertTrue(is_close(datetime.now() - timedelta(days=1),
                        _parse_dt('1day')))
        # hours
        self.assertTrue(is_close(datetime.now() - timedelta(hours=2),
                        _parse_dt('2h')))
        self.assertTrue(is_close(datetime.now() - timedelta(hours=2),
                        _parse_dt('2hours')))
        self.assertTrue(is_close(datetime.now() - timedelta(hours=2),
                        _parse_dt('2 hours')))
        self.assertTrue(is_close(datetime.now() - timedelta(hours=1),
                        _parse_dt('1hour')))
        # minutes
        self.assertTrue(is_close(datetime.now() - timedelta(minutes=2),
                        _parse_dt('2m')))
        self.assertTrue(is_close(datetime.now() - timedelta(minutes=2),
                        _parse_dt('2min')))
        self.assertTrue(is_close(datetime.now() - timedelta(minutes=2),
                        _parse_dt('2 min')))
        # seconds
        self.assertTrue(is_close(datetime.now() - timedelta(seconds=20),
                        _parse_dt('20s')))
        self.assertTrue(is_close(datetime.now() - timedelta(seconds=20),
                        _parse_dt('20sec')))
        self.assertTrue(is_close(datetime.now() - timedelta(seconds=20),
                        _parse_dt('20 sec')))

    def test_serialize_json(self):
        '''Test function for serializing json with dates'''
        self.assertEqual('{}', _serialize_json({}))
        self.assertEqual('"2030-01-02"', _serialize_json(date(2030, 1, 2)))
        self.assertEqual('"2030-01-02T03:04:05"',
                         _serialize_json(datetime(2030, 1, 2, 3, 4, 5)))

    def test_j(self):
        '''Test function for serializing to json and encoding bytes'''
        self.assertEqual(b'{}', _j({}))
        self.assertEqual(b'"2030-01-02"', _j(date(2030, 1, 2)))
        # avoid indent comparison by decoding json again
        self.assertEqual(dict(a=2, b=3),
                         json.loads(_j(a=2, b=3).decode('utf8')))
