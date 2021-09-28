from yhttp import statuscode, json

from .rollup import app


index = app.route(r'/|\*')


@index
@statuscode('204 No Content')
def options(req):
    req.response.headers['Allow'] = 'OPTIONS, INFO'


@index
@json
@statuscode('200 Ok')
def info(req):
    import chord

    return dict(
        version=chord.__version__
    )
