import os
import unittest
import uuid
import json
import mock

from simpletcd.etcd import EtcdHTTPConnect, Etcd

class MockEtcdHTTPConnect(EtcdHTTPConnect):

    def __init__(self, fixture=None):
        super(MockEtcdHTTPConnect, self).__init__()

        self.fixture = fixture


    def request(self, method, uri, data=None):
        data = self.fixture.get(method.lower(), {})
        r = None
        for key, item in data.iteritems():
            if item['uri'] == uri:
                r = json.dumps(item['response'])
                break

        if r is None:
            raise KeyError('Response for uri "%s" has not been defined in test fixture' % uri)

        return (200, r)


class EtcdTest(unittest.TestCase):

    def setUp(self):
        cwd = os.path.dirname(os.path.abspath(__file__))
        fname = os.path.join(cwd, 'http_response_fixture.json')

        with open(fname) as f:
            self.fixture = json.load(f)

        self.etcd = Etcd(conn_cls=MockEtcdHTTPConnect, fixture=self.fixture)


    def tearDown(self):
        pass


    def test_get_key(self):
        requests = self.fixture.get('get')

        for key, data in requests.iteritems():
            result = self.etcd.get(key)
            self.assertTrue(result == data['obj'])


    def test_get_key_raw(self):
        requests = self.fixture.get('get')

        for key, data in requests.iteritems():
            result = self.etcd.get(key, raw=True)
            self.assertTrue(result == data['response'])

    def test_put_key(self):
        requests = self.fixture.get('put')

        for key, data in requests.iteritems():
            result = self.etcd.put(key, data['data'])
            self.assertTrue(result)

