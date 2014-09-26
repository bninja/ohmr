====
ohmr
====

.. image:: https://travis-ci.org/bninja/ohmr.png
   :target: https://travis-ci.org/bninja/ohmr

.. image:: https://coveralls.io/repos/bninja/ohmr/badge.png
   :target: https://coveralls.io/r/bninja/ohmr

For generating, encoding and managing runtime trace ids. These are typically
used to link side-effects:

- db records
- search documents
- log entries
- ...

for things like debugging, auditing, isolation, etc. Get it like:

.. code:: bash

   $ pip install ohmr

To use it first create a tracer e.g. like:

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
