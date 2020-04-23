from google.appengine.ext import ndb

from myuser import MyUser
from posts import Post


class TaskBoard(ndb.Model):
    creator = ndb.KeyProperty(kind=MyUser)
    creator_name = ndb.StringProperty()
    creator_id = ndb.StringProperty()
    # name = ndb.StringProperty()
    members_id = ndb.StringProperty(repeated=True)
    post = ndb.StructuredProperty(Post, repeated=True)
