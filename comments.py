from google.appengine.ext import ndb


class Comments(ndb.Model):
    comment = ndb.StringProperty()
    commenter = ndb.StringProperty()
