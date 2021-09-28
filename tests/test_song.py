from pony.orm import db_session
from bddrest import status, response, when

from chord.models import Artist
from chord.constants import PAGESIZE_MAX


@db_session
def test_song_options(app):
    foo = Artist(title='foo')
    foo.flush()
    with app(f'/artists/artist_id: {foo.id}/songs', 'OPTIONS'):
        assert status == 204
        assert response.headers['Allow'] == 'OPTIONS, GET'

        when(url_parameters=dict(artist_id=2))
        assert status == 404


@db_session
def test_song_get(app):
    foo = Artist(title='foo')
    foo.flush()

    with app(f'/artists/artist_id: {foo.id}/songs'):
        assert status == 200
        assert response.json == []

        # Mockup data
        bar = foo.songs.create(
            title='bar',
            key='Am',
            rhythm='3/4',
            poem='Lorem ipsum.',
        )
        foo.flush()
        when()
        assert status == 200
        assert response.json == [
            {
                'id': bar.id,
                'title': bar.title,
                'key': bar.key,
                'rhythm': bar.rhythm,
                'poem': bar.poem,
                'verified': bar.verified,
                'visible': bar.visible,
                'artist': {
                    'id': foo.id,
                    'title': foo.title
                }
            }
        ]

        # Get with body!
        when(verb='GET', form=dict(foo='bar'))
        assert status == '400 Body Not Allowed'


@db_session
def test_song_get_pagination(app):
    # Mockup data
    foo = Artist(title='foo')

    for j in range(30):
        foo.songs.create(
            title=f'song #{j}',
            key='Am',
            rhythm='3/4',
            poem='Lorem ipsum.'
        )

    foo.flush()

    with app(f'/artists/artist_id: {foo.id}/songs'):
        assert status == 200
        assert len(response.json) == 20

        when(query=dict(page=2))
        assert status == 200
        assert len(response.json) == 10

        when(query=dict(page=2, pagesize=5))
        assert status == 200
        assert len(response.json) == 5

        when(query=dict(pagesize=50))
        assert status == 200
        assert len(response.json) == 30

        when(query=dict(pagesize=PAGESIZE_MAX + 1))
        assert status == '400 Maximum allowed value for field pagesize is 100'


@db_session
def test_songs_get_one(app):
    foo = Artist(title='foo')
    foo.flush()

    with app(f'/artists/artist_id: {foo.id}/songs/id: 1'):
        assert status == 404

        # Mockup data
        bar = foo.songs.create(
            title='bar',
            key='Am',
            rhythm='3/4',
            poem='Lorem ipsum.'
        )
        when()
        assert status == 200
        assert response.json == {
            'id': bar.id,
            'title': bar.title,
            'key': bar.key,
            'rhythm': bar.rhythm,
            'poem': bar.poem,
            'verified': bar.verified,
            'visible': bar.visible,
            'artist': {
                'id': foo.id,
                'title': foo.title
            }
        }

        # Get with body!
        when(form=dict(foo='bar'))
        assert status == '400 Body Not Allowed'
