import os
import re
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

from myuser import MyUser



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape', 'jinja2.ext.loopcontrols'],
    autoescape=True
)


class Search(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        login_status = ''
        user = users.get_current_user()
        search = False

        if user:
            url = users.create_logout_url('/')
            login_status = 'Logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        total_query = MyUser.query()

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

        # POST COUNT
        post_count = 0
        for i in myuser.users_posts_key:
            post_count = post_count + 1

        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,
            'total_query': total_query,
            'user_email': user.email(),
            'user_email_for_search': user.email(),
            'following_count': following_count,
            'followers_count': followers_count,
            'post_count': post_count,
            'search': search,
            'myuser': myuser
        }

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        login_status = ''
        user = users.get_current_user()
        search = True

        if user:
            url = users.create_logout_url(self.request.uri)
            login_status = 'Logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        action = self.request.get('button')

        if action == 'Search':
            username_search = self.request.get('search')

        # SEARCH FOR USERS
        total_users = []
        total_query = []

        query = MyUser.query()

        for i in query:
            total_users.append(i.email)

        regext_search = re.compile('^{username_search}'.format(username_search=username_search))
        regext_result = list(filter(regext_search.match, total_users))

        for results in regext_result:
            search_query = MyUser.query(MyUser.email == results).fetch()
            total_query.append(search_query)

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

        # POST COUNT
        post_count = 0
        for i in myuser.users_posts_key:
            post_count = post_count + 1

        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,
            'total_query': total_query,
            'user_email_for_search': user.email(),
            'following_count': following_count,
            'followers_count': followers_count,
            'post_count': post_count,
            'search': search,
            'myuser': myuser
        }

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))


