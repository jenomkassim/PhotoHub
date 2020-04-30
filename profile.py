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

        followers_id = []
        following_id = []

        for f in myuser.followers:
            followers_id.append(f)

        for fl in myuser.following:
            following_id.append(fl)

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
            'following_count': following_count,
            'followers_id': followers_id,
            'following_id': following_id
        }

        template = JINJA_ENVIRONMENT.get_template('profile.html')
        self.response.write(template.render(template_values))


class OtherUsersProfile(webapp2.RequestHandler):
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

        idd = self.request.get('id')
        user_profile_key = ndb.Key(urlsafe=idd)
        user_profile_id = user_profile_key.id()

        user_profile_deets = ndb.Key('MyUser', user_profile_id).get()

        followers_id = []
        following_id = []

        for f in user_profile_deets.followers:
            followers_id.append(f)

        for fl in user_profile_deets.following:
            following_id.append(fl)

        # FOLLOWERS COUNT
        followers_count = 0

        for i in user_profile_deets.followers:
            followers_count = followers_count + 1

        # FOLLOWING COUNT
        following_count = 0

        for i in user_profile_deets.following:
            following_count = following_count + 1

# -------------------------------------------------------------------------------------------------

        current_user_followers_id = []
        current_user_following_id = []

        for f in myuser.followers:
            current_user_followers_id.append(f)

        for fl in myuser.following:
            current_user_following_id.append(fl)

        # FOLLOWERS COUNT
        current_user_followers_count = 0

        for i in myuser.followers:
            current_user_followers_count = current_user_followers_count + 1

        # FOLLOWING COUNT
        current_user_following_count = 0

        for i in myuser.following:
            current_user_following_count = current_user_following_count + 1

        # POST COUNT
        current_user_post_count = 0
        for i in myuser.users_posts_key:
            current_user_post_count = current_user_post_count + 1

#------------------------------------------------------------------------------------------------

        # GET USERs NAME
        users_first_name = user_profile_deets.email
        users_first_name = users_first_name.split("@")[0]


        template_values = {
            'url': url,
            'user': user,
            'login_status': login_status,
            'user_email': user.email(),
            'myuser_key': myuser_key,
            'upload_url': blobstore.create_upload_url('/upload'),
            'all_posts': user_profile_deets.users_posts_key,
            'Post': Post,
            'MyUser': MyUser,
            'myuser': myuser,
            'followers_count': followers_count,
            'following_count': following_count,
            'user_profile_deets': user_profile_deets,
            'user_id': user.user_id(),
            'followers_id': followers_id,
            'following_id': following_id,
            'current_user_following_count': current_user_following_count,
            'current_user_followers_count': current_user_followers_count,
            'current_user_post_count': current_user_post_count,
            'users_first_name': users_first_name
        }

        template = JINJA_ENVIRONMENT.get_template('users_profile.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        idd = self.request.get('id')
        user_profile_key = ndb.Key(urlsafe=idd)
        user_profile_id = user_profile_key.id()

        # USER PROFILE DETAILS TO FOLLOW
        user_profile_deets = ndb.Key('MyUser', user_profile_id).get()

        # GET USER KEY
        action = self.request.get('button')

        if action == 'Follow':
            user_info = self.request.get('user_info')

            # GET NEW FOLLWER DETAILS
            new_follower = ndb.Key('MyUser', user_info).get()

            # PUT NEW FOLLOWER IN USER'S FOLLOWERS PAGE
            user_profile_deets.followers.append(new_follower.key.id())
            user_profile_deets.put()

            # UPDATE THE USERS PROFILE TO REFLECT THE NEW ACCOUNT THAT HAS JUST BEEN FOLLOWED
            new_follower.following.append(user_profile_deets.key.id())
            new_follower.timeline.append(user_profile_deets.key.id())
            new_follower.put()

            self.redirect('/user_profile?id=' + str(idd))

        if action == 'Unfollow':
            user_info = self.request.get('user_info')

            # UNFOLLOW USER
            for i, followers in enumerate(user_profile_deets.followers):
                if followers == user_info:
                    del user_profile_deets.followers[i]

            user_profile_deets.put()

            # GET CURRENT USER DETAILS
            new_follower = ndb.Key('MyUser', user_info).get()

            # UPDATE THE USERS PROFILE TO REFLECT THE NEW ACCOUNT THAT HAS JUST BEEN UNFOLLOWED
            new_follower.following.remove(user_profile_deets.key.id())
            new_follower.timeline.remove(user_profile_deets.key.id())
            new_follower.put()

            self.redirect('/user_profile?id=' + str(idd))


class UsersFollowers(webapp2.RequestHandler):
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

        idd = self.request.get('id')
        user_profile_key = ndb.Key(urlsafe=idd)
        user_profile_id = user_profile_key.id()

        user_profile_deets = ndb.Key('MyUser', user_profile_id).get()

        followers_id = []
        following_id = []

        for f in user_profile_deets.followers:
            followers_id.append(f)

        for fl in user_profile_deets.following:
            following_id.append(fl)

        # FOLLOWERS COUNT
        followers_count = 0

        for i in user_profile_deets.followers:
            followers_count = followers_count + 1

        # FOLLOWING COUNT
        following_count = 0

        for i in user_profile_deets.following:
            following_count = following_count + 1

        template_values = {
            'url': url,
            'user': user,
            'login_status': login_status,
            'user_email': user.email(),
            'myuser_key': myuser_key,
            'upload_url': blobstore.create_upload_url('/upload'),
            'all_posts': user_profile_deets.users_posts_key,
            'Post': Post,
            'MyUser': MyUser,
            'myuser': myuser,
            'followers_count': followers_count,
            'following_count': following_count,
            'user_profile_deets': user_profile_deets,
            'user_id': user.user_id(),
            'followers_id': followers_id,
            'following_id': following_id
        }

        template = JINJA_ENVIRONMENT.get_template('users_followers.html')
        self.response.write(template.render(template_values))


class UsersFollowing(webapp2.RequestHandler):
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

        idd = self.request.get('id')
        user_profile_key = ndb.Key(urlsafe=idd)
        user_profile_id = user_profile_key.id()

        user_profile_deets = ndb.Key('MyUser', user_profile_id).get()

        followers_id = []
        following_id = []

        for f in user_profile_deets.followers:
            followers_id.append(f)

        for fl in user_profile_deets.following:
            following_id.append(fl)

        # FOLLOWERS COUNT
        followers_count = 0

        for i in user_profile_deets.followers:
            followers_count = followers_count + 1

        # FOLLOWING COUNT
        following_count = 0

        for i in user_profile_deets.following:
            following_count = following_count + 1

        template_values = {
            'url': url,
            'user': user,
            'login_status': login_status,
            'user_email': user.email(),
            'myuser_key': myuser_key,
            'upload_url': blobstore.create_upload_url('/upload'),
            'all_posts': user_profile_deets.users_posts_key,
            'Post': Post,
            'MyUser': MyUser,
            'myuser': myuser,
            'followers_count': followers_count,
            'following_count': following_count,
            'user_profile_deets': user_profile_deets,
            'user_id': user.user_id(),
            'followers_id': followers_id,
            'following_id': following_id
        }

        template = JINJA_ENVIRONMENT.get_template('users_following.html')
        self.response.write(template.render(template_values))




