from google.appengine.ext import ndb

# model for searches
class Search(ndb.Model):
    email = ndb.StringProperty()
    type = ndb.StringProperty()
    value = ndb.StringProperty()
    plot = ndb.StringProperty()
    # if the user search the same value more than once,
    # the counter is incremented accordingly
    counter = ndb.IntegerProperty(default=1)
