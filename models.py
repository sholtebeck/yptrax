"""
ndb.py

App Engine datastore models for Yptrax app

"""


from google.appengine.ext import ndb

class Track(ndb.Model):
    track_id = db.IntegerProperty(required=True)
    name = ndb.StringProperty()
    artist = ndb.StringProperty()
    album = ndb.StringProperty()
    genre = ndb.StringProperty()
    grouping = ndb.StringProperty()
    composer = ndb.StringProperty()
    kind = ndb.StringProperty()
    total_time = ndb.IntegerProperty()
    size = ndb.IntegerProperty()
    year = ndb.IntegerProperty()
    track_number = ndb.IntegerProperty()
    track_count = ndb.IntegerProperty()
    play_count = ndb.IntegerProperty()
    play_date = ndb.StringProperty()
    play_date_utc = ndb.StringProperty()
    file_folder_count = ndb.IntegerProperty()
    library_folder_count = ndb.IntegerProperty()
    artwork_count = ndb.IntegerProperty()
    track_type = ndb.StringProperty()
    location = ndb.StringProperty()
    persistent_id = ndb.StringProperty()
    date_added = ndb.StringProperty()
    date_modified = ndb.StringProperty()

