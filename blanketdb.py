#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''A simple HTTP accessible database for IoT projects.'''

__author__ = 'luphord'
__email__ = 'luphord@protonmail.com'
__version__ = '0.1.0'

import json
import sqlite3
import urllib.parse
from datetime import datetime, date, timedelta


def _parse_form(form_s):
    '''Parse url encoded form and convert numerical types.'''
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
    '''Parse string using custom differential date formats like "2 days".'''
    if not s:
        return ''
    s = str(s)
    if s.lower() == 'today':
        return date.today()
    elif s.lower() == 'yesterday':
        return date.today() - timedelta(days=1)
    elif s.lower().endswith('days') \
            or s.lower().endswith('day') \
            or s.lower().endswith('d'):
        try:
            days = int(s.split('d')[0])
        except ValueError:
            return ''
        return datetime.now() - timedelta(days=days)
    elif s.lower().endswith('hours') \
            or s.lower().endswith('hour') \
            or s.lower().endswith('h'):
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


def _serialize_json(data, indent=2):
    '''Serialize to json supporting dates.'''
    return json.dumps(data, indent=indent, default=_json_default)


def _j(obj_to_serialize=None, **kwargs):
    '''Serialize `obj_to_serialize` or keyword arguments as dict to json
       and encode to bytes.'''
    if obj_to_serialize is None:
        obj_to_serialize = kwargs
    return _serialize_json(obj_to_serialize).encode('utf8')


_HTTP_STATUS_CODES = {
    200: '200 OK',
    201: '201 Created',
    400: '400 Bad Request',
    404: '404 Not found',
    405: '405 Method Not Allowed',
    415: '415 Unsupported Media Type'
}


class BlanketDB:
    '''A simple HTTP accessible database for IoT projects'''

    _SOURCE = 'FROM blanketdb WHERE (? OR bucket=?) AND rowid>=? ' + \
              'AND timestamp>=? AND (? OR rowid<?) AND (? OR timestamp<?)'
    _QUERY = 'SELECT rowid, * ' + _SOURCE + \
             ' ORDER BY (? * rowid) DESC LIMIT ?;'
    _DELETE = 'DELETE ' + _SOURCE + ';'

    def __init__(self, connection_string, now=datetime.now):
        '''Initialize `BlanketDB` instance using a `connection_string`
           that can be understood by SQLite. `now` should be a function
           returning the current datetime (or a suitable test replacement).
        '''
        self.connection = sqlite3.connect(connection_string,
                                          detect_types=sqlite3.PARSE_DECLTYPES)
        with self.connection as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS blanketdb ' +
                         '(bucket text, timestamp timestamp, data text);')
        self.now = now

    def store(self, data, bucket='default'):
        '''Serialize `data` to json and store it under `bucket`.'''
        entry_id = None
        bucket = bucket.lower()
        timestamp = self.now()
        with self.connection as conn:
            c = conn.cursor()
            c.execute('INSERT INTO blanketdb VALUES (?, ?, ?);',
                      (bucket, timestamp, _serialize_json(data, indent=None)))
            entry_id = c.lastrowid
        return dict(id=entry_id, bucket=bucket,
                    timestamp=timestamp.isoformat(), data=data)

    def store_dict(self, bucket='default', **kwargs):
        '''Serialize key word args to json and store under `bucket`.'''
        return self.store(kwargs, bucket)

    def __getitem__(self, entry_id):
        '''Get a stored entry by its `entry_id`.
           Return None if no entry exists for that ID.
        '''
        with self.connection as conn:
            c = conn.execute('SELECT rowid, * FROM blanketdb WHERE rowid=?;',
                             (entry_id,))
            res = c.fetchone()
            if res:
                id, bucket, timestamp, data = res
                return dict(id=id, bucket=bucket,
                            timestamp=timestamp, data=json.loads(data))
            else:
                return None

    def query(self, bucket=None,
              since_id=0, since='',
              before_id=None, before=None,
              limit=-1, newest_first=True):
        '''Query this `BlanketDB` instance using various optional filters.
           `since` and `since_id` are inclusive, `before` and `before` are
           exclusive regarding the specified value.'''
        is_bucket_requested = bool(bucket)
        if is_bucket_requested:
            bucket = bucket.lower()
        since = _parse_dt(since)
        before = _parse_dt(before)
        with self.connection as conn:
            c = conn.execute(BlanketDB._QUERY,
                             (not is_bucket_requested, bucket,
                              since_id, since,
                              not before_id, before_id, not before, before,
                              1 if newest_first else -1, limit))
            for id, bucket, timestamp, data in c.fetchall():
                yield dict(id=id, bucket=bucket,
                           timestamp=timestamp, data=json.loads(data))

    def __iter__(self):
        '''Iterate over all entries stored in this `BlanketDB` instance.'''
        with self.connection as conn:
            c = conn.execute('SELECT rowid, * FROM blanketdb;')
            for id, bucket, timestamp, data in c.fetchall():
                yield dict(id=id, bucket=bucket,
                           timestamp=timestamp, data=json.loads(data))

    def __delitem__(self, entry_id):
        '''Delete an entry by its `entry_id`.'''
        with self.connection as conn:
            conn.execute('DELETE FROM blanketdb WHERE rowid=?;', (entry_id,))

    def delete(self, bucket=None,
               since_id=0, since='',
               before_id=None, before=None):
        '''Delete entries from this `BlanketDB` instance
           using various filters. `since` and `since_id` are inclusive,
           `before` and `before` are exclusive regarding the specified value.
        '''
        is_bucket_requested = bool(bucket)
        if is_bucket_requested:
            bucket = bucket.lower()
        since = _parse_dt(since)
        before = _parse_dt(before)
        with self.connection as conn:
            conn.execute(BlanketDB._DELETE, (not is_bucket_requested, bucket,
                         since_id, since,
                         not before_id, before_id, not before, before))
            return conn.execute('select changes();').fetchone()[0]

    def __call__(self, env, start_response):
        '''WSGI conform callable method.'''
        def start_json_response(status,
                                headers=[('Content-Type',
                                          'application/json')]):
            start_response(_HTTP_STATUS_CODES[status], headers)

        path = (env['PATH_INFO'] or '/').lower()
        method = env['REQUEST_METHOD'].upper()
        qs = _parse_form(env['QUERY_STRING'])
        try:
            show_meta = qs.get('meta', True)
            since_id = qs.get('since_id', 0)
            before_id = qs.get('before_id', None)
            since = _parse_dt(qs.get('since', None))
            before = _parse_dt(qs.get('before', None))
            limit = int(qs.get('limit', -1))
            newest_first = bool(qs.get('newest_first', True))
        except Exception:
            start_json_response(400)
            yield _j(message='An error occured while' +
                             ' parsing the query parameters',
                     parameters=qs)
            return

        if method == 'GET':
            if path.startswith('/_entry/'):
                try:
                    entry_id = int(path[8:])
                except ValueError:
                    start_json_response(400)
                    yield _j(message='Path does not contain' +
                                     ' a valid integer ID',
                             path=path)
                    return
                entry = self[entry_id]
                if entry:
                    start_json_response(200)
                    yield _j(entry if show_meta else entry['data'])
                else:
                    start_json_response(404)
                    yield _j(message='Entry does not exist', id=entry_id)
            else:
                start_json_response(200)
                bucket = path[1:]
                if not bucket:
                    bucket = None  # make it a little more explicit
                entries = list(self.query(bucket, since_id, since,
                               before_id, before, limit, newest_first))
                last_id = max((entry['id'] for entry in entries), default=None)
                entries = [entry if show_meta else entry['data']
                           for entry in entries]
                yield _j(bucket_requested=bucket,
                         since_id=since_id,
                         since=since if since else None,
                         before_id=before_id,
                         before=before if before else None,
                         number_of_entries=len(entries),
                         last_id=last_id,
                         limit=limit if limit > -1 else None,
                         newest_first=newest_first,
                         entries=entries)

        elif method == 'POST':
            if path == '/_entry' or path.startswith('/_entry/'):
                start_json_response(405)
                yield _j(message='The HTTP method is not allowed' +
                                 ' for this path',
                         path=path, method=method)
                return
            try:
                request_body_size = int(env.get('CONTENT_LENGTH', 0))
            except ValueError:
                request_body_size = 0
            request_body = env['wsgi.input'].read(request_body_size)
            bucket = 'default' if path == '/' else path[1:]
            content_type = env.get('CONTENT_TYPE', 'application/json').lower()
            if content_type.startswith('application/json'):
                if request_body == b'':
                    data = None
                else:
                    # ToDo: handle parser errors
                    data = json.loads(request_body.decode('utf8'))
            elif content_type.startswith('application/x-www-form-urlencoded'):
                data = _parse_form(request_body.decode('utf8'))
            else:
                start_json_response(415)
                yield _j(message='Supported media types are application/json' +
                                 ' and application/x-www-form-urlencoded',
                         media_type=content_type)
                return
            entry = self.store(data, bucket=bucket)
            start_json_response(201)
            yield _j(entry)

        elif method == 'DELETE':
            if path.startswith('/_entry/'):
                try:
                    entry_id = int(path[8:])
                except ValueError:
                    start_json_response(400)
                    yield _j(message='Path does not contain' +
                                     ' a valid integer ID',
                             path=path)
                    return
                entry = self[entry_id]
                if entry:
                    start_json_response(200)
                    del self[entry_id]
                    yield _j(entry)
                else:
                    start_json_response(404)
                    yield _j(message='Entry does not exist', id=entry_id)
            else:
                bucket = path[1:]
                if not bucket:
                    bucket = None  # make it a little more explicit
                n = self.delete(bucket, since_id, since, before_id, before)
                start_json_response(200)
                yield _j(bucket_requested=bucket,
                         since_id=since_id,
                         since=since if since else None,
                         before_id=before_id,
                         before=before if before else None,
                         number_of_entries_deleted=n)

        else:
            start_json_response(405)
            yield _j(message='The HTTP method is not allowed for this path',
                     path=path, method=method)
