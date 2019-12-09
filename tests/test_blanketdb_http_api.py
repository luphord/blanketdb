#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Test HTTP API of BlanketDB.'''


import unittest
from datetime import datetime, timedelta

from webtest import TestApp

from blanketdb import BlanketDB


class TestBlanketDBHttpApi(unittest.TestCase):
    '''Test HTTP API of BlanketDB.'''

    def setUp(self):
        self.next_date = datetime(2022, 7, 15)
        self.db = BlanketDB(':memory:', lambda: self.next_date)
        self.app = TestApp(self.db)

    def tearDown(self):
        pass

    def test_basic_web_requests(self):
        '''Test basic web requests'''
        resp = self.app.get('/', status=200)
        self.assertEqual(0, len(resp.json['entries']))
        self.assertEqual(0, resp.json['number_of_entries'])
        self.app.get('/_entry/123', status=404)
        self.app.get('/_entry/', status=400)

    def test_method_not_allowed_requests(self):
        '''Test several method/route combinations which are not allowed'''
        self.app.post('/_entry', status=405)
        self.app.post('/_entry/123', status=405)
        self.app.put('/_entry/', status=405)
        self.app.put('/_entry/123', status=405)
        self.app.put('/anything', status=405)

    def test_create_entry_requests(self):
        '''Test entry creation by request'''
        self.app.post('/', status=201)
        self.app.post('/otherbucket', status=201)
        self.app.post('/', dict(a=1), status=201)  # post form
        self.app.post_json('/', dict(a=1), status=201)  # post json
        self.assertEqual(4, len(self.app.get('/', status=200).json['entries']))
        self.assertEqual(1, len(self.app.get('/otherbucket', status=200)
                                        .json['entries']))
        self.assertEqual(3, len(self.app.get('/default', status=200)
                                        .json['entries']))

    def test_query_requests(self):
        '''Test querying'''
        for i in range(10):
            resp = self.app.post('/testbucket', dict(number=i), status=201)
            if i == 0:
                self.assertEqual(1, resp.json['id'],
                                 'SQLite id changed unexpected')
            if i == 4:
                after_four = self.next_date
            self.next_date += timedelta(seconds=4)
        self.assertEqual(10, self.app.get('/testbucket', status=200)
                                     .json['number_of_entries'])
        self.assertEqual(0, self.app.get('/testbucket2', status=200)
                                    .json['number_of_entries'])
        self.assertEqual(10, self.app.get('/testbucket', dict(since_id=1),
                                          status=200)
                                     .json['number_of_entries'])
        self.assertEqual(9, self.app.get('/testbucket', dict(since_id=2),
                                         status=200)
                                    .json['number_of_entries'])
        self.assertEqual(8, self.app.get('/testbucket', dict(since_id=3),
                                         status=200)
                                    .json['number_of_entries'])
        self.assertEqual(2, self.app.get('/testbucket', dict(before_id=3),
                                         status=200)
                                    .json['number_of_entries'])
        self.assertEqual(6, self.app.get('/testbucket', dict(since=after_four),
                                         status=200)
                                    .json['number_of_entries'])
        self.assertEqual(4, self.app.get('/testbucket',
                                         dict(before=after_four),
                                         status=200)
                                    .json['number_of_entries'])
        self.assertEqual(2, self.app.get('/testbucket',
                                         dict(before=after_four, limit=2),
                                         status=200)
                                    .json['number_of_entries'])
        i = 10
        for entry in self.app.get('/', dict(newest_first=True), status=200) \
                             .json['entries']:
            self.assertGreater(i, entry['data']['number'])
            i = entry['data']['number']
        i = -1
        for entry in self.app.get('/', dict(newest_first=False), status=200) \
                             .json['entries']:
            self.assertLess(i, entry['data']['number'])
            i = entry['data']['number']

    def test_delete_requests(self):
        '''Test entry deletion'''
        # delete by id
        resp = self.app.post('/', status=201)
        id_created = resp.json['id']
        self.assertTrue(isinstance(id_created, int))
        self.app.get('/_entry/{0}'.format(id_created), status=200)
        self.app.delete('/_entry/{0}'.format(id_created), status=200)
        self.app.get('/_entry/{0}'.format(id_created), status=404)
        self.app.delete('/_entry/{0}'.format(id_created), status=404)
        # delete by bucket
        for i in range(3):
            self.app.post('/', status=201)
        for i in range(4):
            self.app.post('/otherbucket', status=201)
        self.assertEqual(3, self.app.get('/default', status=200)
                                    .json['number_of_entries'])
        self.app.delete('/default', status=200)
        self.assertEqual(0, self.app.get('/default', status=200)
                                    .json['number_of_entries'])
        self.assertEqual(4, self.app.get('/otherbucket', status=200)
                                    .json['number_of_entries'])
        self.app.delete('/otherbucket', status=200)
        self.assertEqual(0, self.app.get('/otherbucket', status=200)
                                    .json['number_of_entries'])
        self.app.delete('/otherbucket', status=200)  # still 200
        for i in range(3):
            self.app.post('/', status=201)
        for i in range(4):
            self.app.post('/otherbucket', status=201)
        self.assertEqual(7, self.app.get('/', status=200)
                                    .json['number_of_entries'])
        self.app.delete('/', status=200)  # deletes all, not default bucket
        self.assertEqual(0, self.app.get('/', status=200)
                                    .json['number_of_entries'])
