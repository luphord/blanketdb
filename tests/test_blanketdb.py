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
        self.assertEqual(1, len(list(self.db)))
        self.assertEqual(data, list(self.db)[0]['data'])
        self.assertEqual(dict(x='test'), self.db.store_dict(x='test')['data'])
        self.assertEqual(2, len(list(self.db)))
