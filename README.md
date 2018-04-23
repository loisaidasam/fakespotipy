# fakespotipy

A fake [spotipy](https://github.com/plamere/spotipy) client. For unit tests and stuff.

## Installation

```
pip install fakespotipy
```

## Usage

```python
# Initialize the client
>>> from fakespotipy import FakeSpotify
>>> client = FakeSpotify()

# 1. Example of a mock object response
# First, set up a mock response
>>> response = {
...     'expires_in': 60,
...     'access_token': 'BQDdKdI1eLRl2ErhCRC0jHdfr_DYEm_ecUuUPq2-dW_txQZeCrA32lNSYOZO7v7rEPXqC846nHlgSeg4m0c3-y05W9ISJRluCXdco4igf8eMhgLojXZb4RbE0vmlH4a06T3TX7Jg-uN1ClYFEkXnCGCA0NBNqkiFYDKlvMWqZExQom-XF-8pr6gV_PpzNJ2eKRRR6_ORp1ABUhtJ_aD8f5W4GexLq1mzpWQLkKE_Fq_LuwE1JhpxxNxRI-FLtzz46Jc',
...     'token_type': 'Bearer',
...     'refresh_token': 'AQDDNE-U4IElufFWfNjlwy7rOn-Kyt2PeIN1Nze2I5rVi7c9Etcx9blVkHVe5liSoKRMbJzS3etlA3sQ-0UqMKxRJ-HN08jrO_1IoDgciSZOaAUaQUiSkBOgtgnmO_tEHCU',
...     'scope': 'user-top-read',
... }

# Prep the client with that response
>>> client.add_response('refresh_access_token', response)

# And trigger it
>>> client.refresh_access_token('refresh_token_str_here')
{'access_token': 'BQDdKdI1eLRl2ErhCRC0jHdfr_DYEm_ecUuUPq2-dW_txQZeCrA32lNSYOZO7v7rEPXqC846nHlgSeg4m0c3-y05W9ISJRluCXdco4igf8eMhgLojXZb4RbE0vmlH4a06T3TX7Jg-uN1ClYFEkXnCGCA0NBNqkiFYDKlvMWqZExQom-XF-8pr6gV_PpzNJ2eKRRR6_ORp1ABUhtJ_aD8f5W4GexLq1mzpWQLkKE_Fq_LuwE1JhpxxNxRI-FLtzz46Jc', 'token_type': 'Bearer', 'expires_in': 60, 'refresh_token': 'AQDDNE-U4IElufFWfNjlwy7rOn-Kyt2PeIN1Nze2I5rVi7c9Etcx9blVkHVe5liSoKRMbJzS3etlA3sQ-0UqMKxRJ-HN08jrO_1IoDgciSZOaAUaQUiSkBOgtgnmO_tEHCU', 'scope': 'user-top-read'}

# If we try again, we get a NotImplementedError
>>> client.refresh_access_token('refresh_token_str_here')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "fakespotipy.py", line 37, in method
    raise NotImplementedError
NotImplementedError

# 2. Example of a mock function response
# First set up the mock function
>>> def refresh_response(refresh_token_str):
...     print "i'm refreshing!"
...     if refresh_token_str == 'foo':
...         raise Exception("Foo! Oh noes!")
...     return {'foo': 'bar'}
... 

# Add it a couple of times (so we can call it twice)
>>> client.add_response('refresh_access_token', refresh_response)
>>> client.add_response('refresh_access_token', refresh_response)

# Trigger it
>>> client.refresh_access_token('refresh_token_str_here')
i'm refreshing!
{'foo': 'bar'}

# Trigger again, using anticipated input to trigger custom Exception
>>> client.refresh_access_token('foo')
i'm refreshing!
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "fakespotipy.py", line 40, in method
    return response(*args, **kwargs)
  File "<stdin>", line 4, in refresh_response
Exception: Foo! Oh noes!

# Try one more time, get NotImplementedError
>>> client.refresh_access_token('foo')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "fakespotipy.py", line 37, in method
    raise NotImplementedError
NotImplementedError
```

## Testing

```
python setup.py test
```
