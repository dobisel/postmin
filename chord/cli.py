import sys
import json
import functools

import easycli
from pony.orm import db_session
from yhttp.ext import pony as ponyext

from .models import Artist, db


error = functools.partial(print, file=sys.stderr)
EXIT_FAILURE = 1


class DuplicateEntryError(Exception):
    pass


class ImportDataSubCommand(easycli.SubCommand):
    __command__ = 'import'
    __arguments__ = [
        easycli.Argument('inputfile', nargs='+'),
        easycli.Argument('--overwrite', action='store_true', default=False),
    ]

    def __call__(self, args):
        from .rollup import app

        status = 0
        ponyext.initialize(db, app.settings.db.url)

        try:
            for filename in args.inputfile:
                try:
                    self.importfile(filename, args.overwrite)
                    print(f'Ok: {filename}')
                except DuplicateEntryError as e:
                    error(str(e))
                    status = EXIT_FAILURE

            return status
        finally:
            ponyext.deinitialize(db)

    @db_session
    def importfile(self, filename, overwrite):
        with open(filename) as f:
            data = json.load(f)

        artistname = data['artist']
        songname = data['song']
        songkey = data['key']
        rhythm = data.get('rhythm')
        poem = data['key']

        artist = Artist.get(title=artistname)
        if artist is None:
            artist = Artist(title=artistname)

        song = artist.songs.select(lambda s: s.title == songname).get()
        if song is None:
            song = artist.songs.create(
                title=songname,
                key=songkey,
                rhythm=rhythm,
                poem=poem
            )

        elif not overwrite:
            raise DuplicateEntryError(
                f'Song {songname} already exists for artist {artistname}.'
            )

        else:
            song.key = songkey
            song.rhythm = rhythm
            song.poem = poem
