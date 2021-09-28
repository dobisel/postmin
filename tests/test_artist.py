from pony.orm import db_session
from bddrest import status, response, when

from chord.models import Artist
from chord.constants import PAGESIZE_MAX


def test_artists_options(app):
    with app('/artists', 'OPTIONS'):
        assert status == 204
        assert response.headers['Allow'] == 'OPTIONS, GET'


@db_session
def test_artists_get(app):
    with app('/artists'):
        assert status == 200
        assert response.json == []

        # Mockup data
        foo = Artist(title='foo')
        foo.songs.create(
            title='bar',
            key='Am',
            poem='Lorem ipsum.',
            rhythm='3/4'
        )
        foo.flush()
        assert foo.to_dict() == {
            'id': 1,
            'title': 'foo',
        }

        when()
        assert status == 200
        assert response.json == [
            {
                'id': 1,
                'title': 'foo',
                'songs': 1,
            }
        ]

        # Get with body!
        when(form=dict(foo='bar'))
        assert status == '400 Body Not Allowed'


@db_session
def test_artists_get_pagination(app):
    # Mockup data
    for i in range(30):
        artist = Artist(
            title=f'artist #{i}'
        )

        for j in range(30):
            artist.songs.create(
                title=f'song #{j}',
                key='Am',
                rhythm='3/4',
                poem='Lorem ipsum.'
            )

    with app('/artists'):
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
def test_artists_get_one(app):
    with app('/artists/id: 1'):
        assert status == 404

        # Mockup data
        foo = Artist(title='foo')
        foo.songs.create(
            title='bar',
            key='Am',
            rhythm='3/4',
            poem='Lorem ipsum.',
        )
        when()
        assert status == 200
        assert response.json == {
            'id': foo.id,
            'title': foo.title,
            'songs': 1,
        }

        # Get with body!
        when(form=dict(foo='bar'))
        assert status == '400 Body Not Allowed'
