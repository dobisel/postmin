from yhttp import statuscode, json, validate, statuses
from pony.orm import db_session, select

from .rollup import app
from .models import Artist
from .constants import PAGESIZE_MAX


artists = app.route(r'/artists')
artist = app.route(r'/artists/(\d+)')


@artists
@statuscode('204 No Content')
def options(req):
    req.response.headers['Allow'] = 'OPTIONS, GET'


@artist
@validate(nobody=True)
@json
@db_session
def get(req, id):
    artist = select(
        (a.id, a.title, len(a.songs))
        for a in Artist
        if a.id == id
    ).get()

    if artist is None:
        raise statuses.notfound()

    id, title, songs = artist
    return dict(
        id=id,
        title=title,
        songs=songs,
    )


@artists
@validate(nobody=True, fields=dict(
    page=dict(type_=int),
    pagesize=dict(
        type_=int,
        maximum=PAGESIZE_MAX
    )
))
@json
@db_session
def get(req, *, page=1, pagesize=20):
    out = []
    query = select(
        (a.id, a.title, len(a.songs))
        for a in Artist
    )
    for id, title, songs in query.page(page, pagesize):
        out.append(dict(
            id=id,
            title=title,
            songs=songs,
        ))

    return out
