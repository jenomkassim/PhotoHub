import os

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb



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


        count = 0

        # for i in total_query:
        #     count = count + 1

        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,
            # 'total_query': total_query,
            'count': count
        }

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):
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

        action = self.request.get('Search')
        count = 0

        if action == 'Search':
            name = self.request.get('vehicleName')

        car_query = Vehicles.query()



        if len(name) == 0 and len(manufacturer) == 0:
            total_query = ndb.get_multi(set(year_query).intersection(battery_query).intersection(range_query)
                                        .intersection(cost_query).intersection(power_query))
            for i in total_query:
                count = count + 1

        else:
            name_query = Vehicles.query(Vehicles.name == name).fetch(keys_only=True)
            manufacturer_query = Vehicles.query(Vehicles.manufacturer == manufacturer).fetch(keys_only=True)
            total_query = ndb.get_multi(set(name_query).intersection(manufacturer_query).intersection(year_query)
                                        .intersection(battery_query).intersection(range_query).intersection(cost_query)
                                        .intersection(power_query))

            for i in total_query:
                count = count + 1

