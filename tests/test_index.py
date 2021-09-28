from bddrest import status, response, when


def test_index_options(app):
    with app('/', 'OPTIONS'):
        assert status == 204
        assert response.headers['Allow'] == 'OPTIONS, INFO'

        when('*')
        assert status == 204
        assert response.headers['Allow'] == 'OPTIONS, INFO'


def test_index_info(app):
    import chord

    with app('/', 'INFO'):
        assert status == 200
        assert response.json == dict(version=chord.__version__)
