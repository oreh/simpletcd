import os 
import json
import httplib
import urllib
import urllib2


DEFAULT_ETCD_PROTOCOL = 'http'
DEFAULT_ETCD_HOST = "127.0.0.1"
DEFAULT_ETCD_PORT = 4001


class EtcdOpsException(Exception):
    def __init__(self, status, content):
        msg = json.dumps({'status': status, 'content': content})
        super(EtcdOpsException, self).__init__(msg)


def parse_etcd_response(data, parent=None):
    result = {}

    if parent is None:
        key = data['key'].split('/')[-1]
        if key == '':
            key = '/'
    else:
        if parent == '/':
            key = data['key'][1:]
        else:
            key = os.path.relpath(data['key'], parent)

    if 'dir' in data and data['dir']:
        result[key] = {}
        for n in data['nodes']:
            result[key].update(parse_etcd_response(n, data['key']))
    else:
        result[key] = data['value']

    return result


def dict_to_records(data, parent_key='/'):
    ''' ToDo: Add doc tests
    '''

    records = {}
    for k, v in data.iteritems():
        key = parent_key + '/' + k

        if type(v) in (str, unicode, int, float):
            records[key] = v
        elif type(v) is dict:
            records.update(dict_to_records(v, parent_key=key))
        else:
            raise ValueError('Cannot convert type %s to etcd data' % type(v))
    return records

class EtcdHTTPConnect(object):

    def request(self, method, uri, params=None):
        method = method.upper()

        opener = urllib2.build_opener(urllib2.HTTPHandler)
        if params is None:
            request = urllib2.Request(uri)
        else:
            request = urllib2.Request(uri, data=urllib.urlencode(params))

        if method in ('PUT', 'DELETE'):
            request.get_method = lambda: method

        rep = opener.open(request)
        return (rep.code, rep.read())

    
class Etcd():
    def __init__(self, host=DEFAULT_ETCD_HOST, port=DEFAULT_ETCD_PORT,
            protocol=DEFAULT_ETCD_PROTOCOL, conn_cls=EtcdHTTPConnect, **kwargs):

        self.protocol = protocol
        self.host = host
        self.port = port
        self.conn = conn_cls(**kwargs)


    def get_uri(self, key):
        if key.startswith('/'):
            key = key[1:]
        return '%s://%s:%s/v2/keys/%s' % (self.protocol, self.host, self.port, key)


    def get(self, key, raw=False):
        if key.startswith('/'):
            key = key[1:]

        uri = self.get_uri(key)+'?recursive=true'
        status, content = self.conn.request('get', uri)

        if status == 200:
            data = json.loads(content)
            if raw:
                return data

            node = data['node']
            if 'dir' in node and node['dir']:
                return parse_etcd_response(node)
            else:
                key = node['key'].split('/')[-1]
                if key == '':
                    key = '/'
                return {key: node['value']}

        raise EtcdOpsException(status, content)


    def delete(self, key):
        uri  = self.get_uri(key)

        status, content = self.conn.request("delete", uri+"?recursive=true")
        if status == 200:
            return True
        raise EtcdOpsException(status, content)


    def put(self, key, data):
        if type(data) in (str, unicode, int, float):
            params = {"value": data}
            status, content = self.conn.request("put", self.get_uri(key), params)
            if status == 200 or status == 201:
                return True
            raise EtcdOpsException(status, content)
        elif isinstance(data, dict):
            records = dict_to_records(data, parent_key=key)

            for k, v in records.iteritems():
                if not self.put(k, v):
                    self.delete_dir(key)
                    return False
            return True
        else:
            raise ValueError('Cannot convert type %s to etcd data' % type(value))

