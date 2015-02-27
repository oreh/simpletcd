# introduction

_simpletcd_ is a simple etcd client that aims to make recursive get/put operations easier. If you are using etcd mainly as a configuration repository or a meta data storage, _simpletcd_ helps to simplify store and retrieve dictionary datawith a single call.


# Install

```
pip install simpletcd
```

# Usage

## Put a value to a key
```python
>> from simpletcd.ectd import Etcd

>> # Etcd can be initallized with specific host (default, 127.0.0.1) and port (default 2379)
>> # e.g. Etcd(host=<host>, port=<port>)
>> etcd = Etcd() 
>> etcd.put('mytestkey', 'test value')

```

## Get a key
```python
>> from simpletcd.ectd import Etcd

>> etcd = Etcd()
>> etcd.get('mytestkey')
{u'mytestkey': u'test value'}

```

## Put multiple keys recursively

```python
>> from simpletcd.ectd import Etcd

>> etcd = Etcd()
>> etcd.put('mytopkey', {'key_0': 'v0', 'key_1': {'key_1_0': 'v1_0', 'key_1_1': 'v1_1'}})

```

## Get multiple keys recursively
```python
>> from simpletcd.ectd import Etcd

>> etcd = Etcd()
>> etcd.put('mytopkey')
{u'mytopkey': {u'key_0': u'v0',
  u'key_1': {u'key_1_0': u'v1_0', u'key_1_1': u'v1_1'}}}
```

Changes:
0.1.1: Change default port to 2379
0.1.0: Initial release
