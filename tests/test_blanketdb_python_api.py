#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Test Python API of BlanketDB.'''


import unittest
from datetime import datetime, timedelta

from blanketdb import BlanketDB


class TestBlanketDBPythonApi(unittest.TestCase):
    '''Test Python API of BlanketDB.'''

    def setUp(self):
        self.next_date = datetime(2022, 7, 15)
        self.db = BlanketDB(':memory:', lambda: self.next_date)

    def tearDown(self):
        pass

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

    def test_query_from_python(self):
        '''Test `BlanketDB.query` method using Python API'''
        for i in range(10):
            resp = self.db.store_dict(bucket='testbucket', number=i)
            if i == 0:
                self.assertEqual(1, resp['id'], 'SQLite id changed unexpected')
            if i == 4:
                after_four = self.next_date
            self.next_date += timedelta(seconds=4)
        self.assertEqual(10, len(list(self.db.query(bucket='testbucket'))))
        self.assertEqual(0, len(list(self.db.query(bucket='testbucket2'))))
        self.assertEqual(10, len(list(self.db.query(since_id=1))))
        self.assertEqual(9, len(list(self.db.query(since_id=2))))
        self.assertEqual(8, len(list(self.db.query(since_id=3))))
        self.assertEqual(2, len(list(self.db.query(before_id=3))))
        self.assertEqual(6, len(list(self.db.query(since=after_four))))
        self.assertEqual(4, len(list(self.db.query(before=after_four))))
        self.assertEqual(2,
                         len(list(self.db.query(before=after_four, limit=2))))
        i = 10
        for entry in self.db.query(newest_first=True):
            self.assertGreater(i, entry['data']['number'])
            i = entry['data']['number']
        i = -1
        for entry in self.db.query(newest_first=False):
            self.assertLess(i, entry['data']['number'])
            i = entry['data']['number']

    def test_delete_from_python(self):
        '''Test `BlanketDB.delete` method using Python API'''
        for i in range(10):
            resp = self.db.store_dict(bucket='testbucket', number=i)
            if i == 0:
                self.assertEqual(1, resp['id'], 'SQLite id changed unexpected')
            if i == 4:
                after_four = self.next_date
            self.next_date += timedelta(seconds=4)
        self.db.delete(since=after_four)
        self.assertEqual(4, len(list(self.db)))
        self.db.delete(before=after_four)
        self.assertEqual(0, len(list(self.db)))
        self.db.store_dict(bucket='testbucket', irrelevant='data')
        self.db.store_dict(bucket='testbucket2', irrelevant='data')
        self.db.delete(bucket='testbucket')
        self.assertEqual(1, len(list(self.db)))
        self.db.delete()
        self.assertEqual(0, len(list(self.db)))
