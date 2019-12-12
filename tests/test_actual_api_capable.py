#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Test HTTP API of BlanketDB.'''


import unittest
from datetime import datetime

from webtest import TestApp
import requests

from blanketdb import BlanketDB


class ActualApiAdapter:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def request_qs(self, method, path, params, exptected_status):
        headers = {'Content-type': 'application/json'}
        response = method(self.base_url + path,
                          headers=headers, params=params)
        response.json = response.json()
        assert response.status_code == exptected_status
        return response

    def request_body(self, method, path, body, exptected_status):
        headers = {'Content-type': 'application/json'}
        response = method(self.base_url + path,
                          headers=headers, json=body)
        response.json = response.json()
        assert response.status_code == exptected_status
        return response

    def get(self, path, params=None, status=200):
        return self.request_qs(requests.get, path, params, status)

    def post(self, path, body=None, status=200):
        return self.request_body(requests.post, path, body, status)

    def post_json(self, path, body=None, status=200):
        return self.request_body(requests.post, path, body, status)

    def put(self, path, body=None, status=200):
        return self.request_body(requests.put, path, body, status)

    def delete(self, path, params=None, status=200):
        return self.request_qs(requests.delete, path, params, status)


class TestBlanketDBActualHttpApiCapable(unittest.TestCase):
    '''Test HTTP API of BlanketDB. These tests also work for an
       "actual" HTTP API, meaning not using webtest.
       Set do_actual_api_calls=True to activate.
    '''

    def setUp(self):
        self.next_date = datetime(2022, 7, 15)
        self.db = BlanketDB(':memory:', lambda: self.next_date)
        do_actual_api_calls = False
        self.app = ActualApiAdapter(base_url='http://localhost:8080') \
            if do_actual_api_calls \
            else TestApp(self.db)

    def tearDown(self):
        pass

    def test_basic_web_requests(self):
        '''Test basic web requests'''
        resp = self.app.get('/', status=200)
        n = len(resp.json['entries'])
        self.assertGreaterEqual(n, 0)
        self.assertEqual(n, resp.json['number_of_entries'])
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
        self.assertGreaterEqual(
            len(self.app.get('/', status=200).json['entries']), 4)
        self.assertGreaterEqual(
            len(self.app.get('/otherbucket', status=200).json['entries']), 1)
        self.assertGreaterEqual(
            len(self.app.get('/default', status=200).json['entries']), 3)

    def test_query_requests(self):
        '''Test querying'''
        for i in range(10):
            resp = self.app.post('/testbucket', dict(number=i), status=201)
            self.assertGreaterEqual(resp.json['id'], 0)
        self.assertGreaterEqual(self.app.get('/testbucket', status=200)
                                    .json['number_of_entries'], 10)
        self.assertEqual(0, self.app.get('/testbucket2', status=200)
                                    .json['number_of_entries'])
        self.assertGreaterEqual(self.app.get('/testbucket', dict(since_id=1),
                                             status=200)
                                    .json['number_of_entries'], 10)
        self.assertGreaterEqual(self.app.get('/testbucket', dict(since_id=2),
                                             status=200)
                                    .json['number_of_entries'], 9)
        self.assertGreaterEqual(self.app.get('/testbucket', dict(since_id=3),
                                             status=200)
                                    .json['number_of_entries'], 8)
        self.assertLessEqual(self.app.get('/testbucket', dict(before_id=3),
                                          status=200)
                                     .json['number_of_entries'], 2)

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
        self.app.delete('/', status=200)
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
