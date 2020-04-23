from google.appengine.ext import ndb


class PostImages(ndb.Model):
    filenames = ndb.StringProperty()
    blobs = ndb.BlobKeyProperty()
