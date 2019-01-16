#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `blanketdb` module."""


import unittest

from blanketdb import BlanketDB


class TestBlanketdb(unittest.TestCase):
    """Tests for `blanketdb` package."""

    def setUp(self):
        """Set up test instance of `BlanketDB`"""
        self.db = BlanketDB(':memory:')

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_storing_from_python(self):
        '''Test storing of data using Python API'''
        data = dict(a=1, b=2)
        stored = self.db.store(data)
        self.assertEqual(data, stored['data'])
        self.assertEqual(data, self.db[stored['id']]['data'])
        self.assertEqual(1, len(list(self.db)))
        self.assertEqual(data, list(self.db)[0]['data'])
        stored2 = self.db.store_dict(x='test')
        self.assertEqual(dict(x='test'), stored2['data'])
        self.assertEqual(dict(x='test'), self.db[stored2['id']]['data'])
        self.assertEqual(2, len(list(self.db)))
        not_in_db_id = abs(stored['id']) + abs(stored2['id']) + 1
        self.assertEqual(None, self.db[not_in_db_id])
        del self.db[stored['id']]
        self.assertEqual(None, self.db[stored['id']])
