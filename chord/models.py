from pony.orm import PrimaryKey, Required, Set, composite_key, Database, \
    Optional


db = Database()


class Artist(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str, unique=True)
    songs = Set(lambda: Song)


class Song(db.Entity):
    id = PrimaryKey(int, auto=True)
    artist = Required(Artist)
    title = Required(str)
    key = Required(str)
    rhythm = Optional(str, nullable=True)
    poem = Required(str)
    composite_key(artist, title)
    visible = Optional(bool, default=False)
    verified = Optional(bool, default=False)
