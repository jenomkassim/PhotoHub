import os

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers

from myuser import MyUser
from post_images import PostImages
from posts import Post

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Profile(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        login_status = ''

        user = users.get_current_user()

        if user:
            url = users.create_logout_url('/')
            login_status = 'Logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        # FOLLOWERS COUNT
        followers_count = 0

        for i in myuser.followers:
            followers_count = followers_count + 1

        # FOLLOWING COUNT
        following_count = 0

        for i in myuser.following:
            following_count = following_count + 1

        template_values = {
            'url': url,
            'user': user,
            'login_status': login_status,
            'user_email': user.email(),
            'myuser_key': myuser_key,
            'upload_url': blobstore.create_upload_url('/upload'),
            'all_posts': myuser.users_posts_key,
            'Post': Post,
            'MyUser': MyUser,
            'myuser': myuser,
            'followers_count': followers_count,
            'following_count': following_count
        }

        template = JINJA_ENVIRONMENT.get_template('profile.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # GET USER KEY
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())

        # GET NEW TASKBOARD NAME
        taskboard_title = self.request.get('taskboard_name')

        # CREATE NEW TASKBOARD

        # Ask Datastore to allocate an ID.
        new_id = ndb.Model.allocate_ids(size=1, parent=myuser_key)[0]

        # Datastore returns us an integer ID that we can use to create the new taskboard key
        new_taskboard_key = ndb.Key('TaskBoard', new_id, parent=myuser_key)

        # Now we can put the values of the new task board into the TaskBoard Datastore
        new_taskboard = TaskBoard(key=new_taskboard_key, creator=myuser_key, creator_name=user.email(),
                                  name=taskboard_title, creator_id=user.user_id())
        new_taskboard.members_id.append(myuser_key.id())
        new_taskboard.put()

        # We also have to pass the details of this task board to the MyUser datastore
        # by retrieving the details of the user to update it by appending the task board key
        new_taskboard_user_ref = MyUser.get_by_id(myuser_key.id())
        new_taskboard_user_ref.td_key.append(new_taskboard.key)
        new_taskboard_user_ref.put()
        self.redirect('/timeline')

