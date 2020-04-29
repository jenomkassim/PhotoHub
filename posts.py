from google.appengine.ext import ndb
from comments import Comments


class Post(ndb.Model):
    creator = ndb.KeyProperty()
    image_key = ndb.KeyProperty()
    image_blob_key = ndb.BlobKeyProperty()
    caption = ndb.StringProperty()
    likes = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    comments = ndb.StructuredProperty(Comments, repeated=True)
