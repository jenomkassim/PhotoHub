import os

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

from myuser import MyUser



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Search(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        login_status = ''
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            login_status = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        total_query = MyUser.query()

        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,
            'total_query' : total_query,
        }

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        login_status = ''
        username_search = ''
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            login_status = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        idd = self.request.get('id')
        user_profile_key = ndb.Key(urlsafe=idd)
        user_profile_id = user_profile_key.id()

        user_profile_deets = ndb.Key('MyUser', user_profile_id).get()

        action = self.request.get('button')
        count = 0

        if action == 'Search':
            username_search = self.request.get('search')

        # SEARCH FOR USERS
        user_search = MyUser.query().fetch()

        name_query = MyUser.query(MyUser.email == username_search).get()
        # self.response.write(name_query)

        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,
            'name_query': name_query,
            'user_profile_deets': user_profile_deets,
            'idd': idd,
        }

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))


