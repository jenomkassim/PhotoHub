from google.appengine.ext import ndb


class Post(ndb.Model):
    caption = ndb.StringProperty()
    likes = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
