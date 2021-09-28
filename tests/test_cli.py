import os
import json

from bddcli import status, stderr, stdout, when, given

from chord.models import Artist


def test_cli_data_import(cliapp, mockupfs, freshdb, dbconn):
    foo = dict(
        artist='foo',
        song='bar',
        key='C',
        rhythm='3/4',
        poem='Lorem Ipsum',
    )
    fsroot = mockupfs(**{
        'foo.json': json.dumps(foo),
        'foo.yml': f'db: {{url: {freshdb}}}'
    })
    configfile = os.path.join(fsroot, 'foo.yml')
    inputfile = os.path.join(fsroot, 'foo.json')

    with cliapp(f'-c {configfile} db import {inputfile}'):
        assert status == 0
        assert stderr == ''
        assert stdout == f'Ok: {inputfile}\n'

        with dbconn(freshdb):
            assert Artist.select().count() == 1
            artist = Artist.get(title='foo')
            assert artist.title == 'foo'
            assert len(artist.songs) == 1
            song = artist.songs.select().get()
            assert song.title == 'bar'

        # Duplicate
        when()
        assert status == 1
        assert stderr == 'Song bar already exists for artist foo.\n'
        assert stdout == ''

        # Overwrite
        when(given + '--overwrite')
        assert status == 0
        assert stderr == ''
        assert stdout == f'Ok: {inputfile}\n'
