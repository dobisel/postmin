from json import load as jsonload
from os.path import join, dirname

from yhttp import Application, json, validate, statuses


__version__ = '0.1.0'


app = Application(version=__version__)
app.settings.debug = False

app.staticdirectory('/', 'public', default=True, fallback=True)
app.ready()
