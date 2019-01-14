#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `blanketdb` package."""


import unittest

from blanketdb import parse_form


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
