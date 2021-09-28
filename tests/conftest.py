import os
import shutil
import tempfile
import functools
import contextlib

import pytest
import bddrest
import bddcli
from yhttp.ext import pony as ponyext
from pony.orm import db_session

import chord
from chord.models import db


@pytest.fixture
def cliapp():
    cliapp = bddcli.Application('chord', 'chord:app.climain')
    return functools.partial(bddcli.Given, cliapp)


@pytest.fixture
def mockupfs():
    temp_directories = []

    def create_nodes(root, **kw):
        for k, v in kw.items():
            name = os.path.join(root, k)

            if isinstance(v, dict):
                os.mkdir(name)
                create_nodes(name, **v)
                continue

            if hasattr(v, 'read'):
                f = v
                v = f.read()
                f.close()

            with open(name, 'w') as f:
                f.write(v)

    def _make_temp_directory(**kw):
        """Structure example: {'a.html': 'Hello', 'b': {}}."""
        root = tempfile.mkdtemp()
        temp_directories.append(root)
        create_nodes(root, **kw)
        return root

    yield _make_temp_directory

    for d in temp_directories:
        shutil.rmtree(d)


@pytest.fixture
def freshdb():
    host = 'localhost'
    user = 'postgres'
    password = 'postgres'
    dbname = 'chord_testdb'
    dbmanager = ponyext.createdbmanager(host, 'postgres', user, password)
    dbmanager.create(dbname, dropifexists=True)
    freshurl = f'postgres://{user}:{password}@{host}/{dbname}'
    yield freshurl
    dbmanager.dropifexists(dbname)


@pytest.fixture
def dbconn():

    @contextlib.contextmanager
    def conn(url=None):
        ponyext.initialize(db, url or chord.app.settings.db.url)
        with db_session:
            yield chord.app.db
        ponyext.deinitialize(db)

    return conn


@pytest.fixture
def app(freshdb):
    chord.app.settings.merge(f'''
      db:
        url: {freshdb}
    ''')
    chord.app.ready()
    yield functools.partial(bddrest.Given, chord.app)
    chord.app.shutdown()
