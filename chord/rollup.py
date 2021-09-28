from yhttp import Application
from yhttp.ext import pony as ponyext

from .cli import ImportDataSubCommand
from .models import db


app = Application()
app.settings.merge('''
db:
  url: postgres://postgres:postgres@localhost/chord
''')
ponyext.install(app, db=db, cliarguments=[
    ImportDataSubCommand,
])
