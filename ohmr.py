"""
For generating, encoding and managing runtime trace ids. These are typically
used to link side-effects:

- db records
- search documents
- log entries
- ...

for things like debugging, auditing, isolation, etc.

First create a tracer:

.. code:: python

    import coid
    import ohmr
    
    
    trace = coid.Tracer(coid.Id(prefix='OHM-'))
    
Then use it, most likely at session begin/resume points, e.g. like:

.. code:: python

    import flask
    
    
    app = flask.Flask('krazy_eyez_killah')
    
    @app.before_request
    def set_trace_id()
        trace.reset()

"""
__version__ = '0.1.0'

import codecs
import contextlib
import threading
import uuid


class Tracer(threading.local):

    generate_id = staticmethod(uuid.uuid4)

    encode_id = staticmethod(lambda x: x.hex)

    def __init__(self, encode_id=None, generate_id=None):
        self._id = None
        self.encode_id = self._as_encode(encode_id or self.encode_id)
        self.generate_id = self._as_generate(generate_id or self.generate_id)

    @classmethod
    def _as_generate(self, value):
        if callable(value):
            return value
        raise TypeError('{0!r} must be a callable'.format(value))

    @classmethod
    def _as_encode(self, value):
        if isinstance(value, (codecs.Codec, codecs.CodecInfo)):
            return value.encode
        if callable(value):
            return value
        if hasattr(value, 'encode') and callable(value):
            return value.encode
        if isinstance(value, basestring):
            return codecs.lookup(value).encode
        raise TypeError('{0!r} must be a callable or codec'.format(value))

    @property
    def id(self):
        if self._id is None:
            self.id = self.encode_id(self.generate_id())
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def reset(self):
        self.id = None

    @contextlib.contextmanager
    def __call__(self, id=None):
        prev = self._id
        self._id = id
        try:
            yield
        finally:
            self._id = prev
