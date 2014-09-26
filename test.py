from __future__ import unicode_literals

import logging
import os
import threading
import uuid

import coid
import pytest

import ohmr


@pytest.fixture(scope='session')
def logging_level():
    return {
        'd': logging.DEBUG, 'debug': logging.DEBUG,
        'i': logging.INFO, 'info': logging.INFO,
        'w': logging.WARN, 'warn': logging.WARN,
    }[os.environ.get('OHMR_TEST_LOG', 'info').lower()]


@pytest.fixture(scope='session', autouse=True)
def logging_config(logging_level):
    logging.basicConfig(level=logging_level)


@pytest.fixture()
def tracer():
    return ohmr.Tracer(coid.Id(prefix='OMG-'))


def test_default():
    tracer = ohmr.Tracer()
    id = tracer.generate_id()
    assert isinstance(id, uuid.UUID)
    assert uuid.UUID(tracer.encode_id(id)) == id


def test_invalid():
    with pytest.raises(LookupError):
        ohmr.Tracer(encode_id='no')
    with pytest.raises(TypeError):
        ohmr.Tracer(generate_id='way')

def test_id(tracer):
    assert isinstance(tracer.id, basestring)
    assert tracer.id.startswith('OMG-')

def test_reset(tracer):
    id = tracer.id
    assert tracer.id == id
    tracer.reset()
    assert tracer.id != id


def test_with(tracer):
    id = tracer.id
    with tracer():
        assert tracer.id != id
    assert tracer.id == id


def test_threading(tracer):

    ids = []

    def append_id():
        ids.append(tracer.id)

    thds = []

    for _ in range(10):
        thd = threading.Thread(target=append_id)
        thd.start()
        thds.append(thd)

    while thds:
        thd = thds.pop()
        thd.join()

    assert 10 == len(ids)
    assert 10 == len(set(ids))
