from yhttp import statuscode, json, validate, statuses
from pony.orm import db_session

from .rollup import app
from .models import Artist, Song
from .constants import PAGESIZE_MAX


songs = app.route(r'/artists/(\d+)/songs')
song = app.route(r'/artists/(\d+)/songs/(\d+)')


@songs
@statuscode('204 No Content')
def options(req, artistid):
    req.response.headers['Allow'] = 'OPTIONS, GET'

    artist = Artist.get(id=artistid)
    if artist is None:
        raise statuses.notfound()


@song
@validate(nobody=True)
@json
@db_session
def get(req, artistid, id):
    song = Song.get(artist=artistid, id=id)
    if song is None:
        raise statuses.notfound()

    d = song.to_dict(related_objects=True)
    d['artist'] = d['artist'].to_dict()
    return d


@songs
@validate(nobody=True, fields=dict(
    page=dict(type_=int),
    pagesize=dict(
        type_=int,
        maximum=PAGESIZE_MAX
    )
))
@json
@db_session
def get(req, artistid, *, page=1, pagesize=20):
    out = []
    for a in Song.select(artist=artistid).page(page, pagesize):
        d = a.to_dict(related_objects=True)
        d['artist'] = d['artist'].to_dict()
        out.append(d)

    return out
