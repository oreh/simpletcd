# introduction

_simpletcd_ is a simple etcd client that aims to make recursive get/put operations easier.


# Install

```
pip install simpletcd
```

# Usage

## Put a value to a key
```python
from simpletcd.ectd import Etcd

etcd = Etcd()
etcd.put('mytestkey', 'test value')

```

## Put multiple keys recursively

```python
from simpletcd.ectd import Etcd

etcd = Etcd()
etcd.put('mytopkey', {'key_0': 'v0', 'key_1': {'key_1_0': 'v1_0', 'key_1_1': 'v1_1'}})

```

## Get a key
```python
from simpletcd.ectd import Etcd

etcd = Etcd()
etcd.get('mytestkey')

```

## Get multiple keys recursively
```python
from simpletcd.ectd import Etcd

etcd = Etcd()
etcd.put('mytopkey')

```

