#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `blanketdb` package."""


import unittest

from datetime import datetime, date, timedelta
from blanketdb import parse_form, _parse_dt

def is_close(dt1, dt2, max_diff_sec=10):
    return abs(dt1.timestamp() - dt2.timestamp()) < max_diff_sec


class TestBlanketdb(unittest.TestCase):
    """Tests for `blanketdb` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_parse_form(self):
        '''Test function for parsing and type converting forms'''
        self.assertEqual(dict(a='b'), parse_form('a=b'))
        self.assertEqual(dict(a='b',c='d'), parse_form('a=b&c=d'))
        self.assertEqual(dict(a=1), parse_form('a=1'))
        self.assertEqual(1.1, parse_form('a=1.1')['a'])
        self.assertEqual(float, type(parse_form('a=1.0')['a']))
        self.assertEqual(dict(a=True), parse_form('a=true'))
        self.assertEqual(dict(a=False), parse_form('a=false'))

    def test_parse_date(self):
        '''Test function for customized date parsing'''
        self.assertEqual('', _parse_dt(''))
        self.assertEqual('2025-02-03', _parse_dt('2025-02-03')) # this function only parses dates in custom format
        self.assertEqual('', _parse_dt(None))
        self.assertEqual(date.today(), _parse_dt('today'))
        self.assertEqual(date.today() - timedelta(days=1), _parse_dt('yesterday'))
        # days
        self.assertTrue(is_close(datetime.now() - timedelta(days=2), _parse_dt('2d')))
        self.assertTrue(is_close(datetime.now() - timedelta(days=2), _parse_dt('2days')))
        self.assertTrue(is_close(datetime.now() - timedelta(days=2), _parse_dt('2 days')))
        self.assertTrue(is_close(datetime.now() - timedelta(days=1), _parse_dt('1day')))
        # hours
        self.assertTrue(is_close(datetime.now() - timedelta(hours=2), _parse_dt('2h')))
        self.assertTrue(is_close(datetime.now() - timedelta(hours=2), _parse_dt('2hours')))
        self.assertTrue(is_close(datetime.now() - timedelta(hours=2), _parse_dt('2 hours')))
        self.assertTrue(is_close(datetime.now() - timedelta(hours=1), _parse_dt('1hour')))
        # minutes
        self.assertTrue(is_close(datetime.now() - timedelta(minutes=2), _parse_dt('2m')))
        self.assertTrue(is_close(datetime.now() - timedelta(minutes=2), _parse_dt('2min')))
        self.assertTrue(is_close(datetime.now() - timedelta(minutes=2), _parse_dt('2 min')))
        # seconds
        self.assertTrue(is_close(datetime.now() - timedelta(seconds=20), _parse_dt('20s')))
        self.assertTrue(is_close(datetime.now() - timedelta(seconds=20), _parse_dt('20sec')))
        self.assertTrue(is_close(datetime.now() - timedelta(seconds=20), _parse_dt('20 sec')))