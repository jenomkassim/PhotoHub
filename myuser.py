from google.appengine.ext import ndb
from post_images import PostImages
from posts import Post


class MyUser(ndb.Model):
    identity = ndb.StringProperty()
    email = ndb.StringProperty()
    following = ndb.StringProperty(repeated=True)
    followers = ndb.StringProperty(repeated=True)
    users_posts_key = ndb.KeyProperty(Post, repeated=True)
    # post = ndb.StructuredProperty(Post, repeated=True)

