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


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        upload = self.get_uploads()[0]
        postCaption = self.request.get('postCaption')
        blobinfo = blobstore.BlobInfo(upload.key())
        filename = blobinfo.filename

        # collection_key = ndb.Key('PostImages', 1)
        # collection = collection_key.get()
        new_image_upload = PostImages()
        new_image_upload.filenames = filename
        new_image_upload.blobs = upload.key()
        new_image_upload.put()

        image_upload_details = Post()
        image_upload_details.caption = postCaption
        image_upload_details.creator = myuser_key
        image_upload_details.image_key = new_image_upload.key
        image_upload_details.image_blob_key = upload.key()
        image_upload_details.put()

        new_post_user_ref = MyUser.get_by_id(myuser_key.id())
        new_post_user_ref.users_posts_key.append(image_upload_details.key)
        new_post_user_ref.put()
        self.redirect('/')
        # self.redirect('/view_photo/%s' % upload.key())


class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        index = int(self.request.get('index'))
        collection_key = ndb.Key('BlobCollection', 1)
        collection = collection_key.get()
        self.send_blob(collection.blobs[index])


# [START download_handler]
class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)
# [END download_handler]


class Timeline(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        welcome = ''
        login_status = ''

        user = users.get_current_user()

        if user:
            welcome = 'Welcome back to the workspace, we missed You!'
            url = users.create_logout_url('/')
            login_status = 'Logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Hurray! Your First Login into the workspace, we hope you enjoy our application!'
                myuser = MyUser(id=user.user_id(),
                                identity=user.user_id(),
                                email=user.email())
                myuser.put()

            # taskboard_user_ref = MyUser.get_by_id(myuser_key.id())
            # taskboard_user_keys = taskboard_user_ref.td_key


        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'


        template_values = {
            'url': url,
            'user': user,
            'welcome': welcome,
            'login_status': login_status,
            'user_email': user.email(),
            'myuser_key': myuser_key,
            'upload_url': blobstore.create_upload_url('/upload'),
            'all_posts': myuser.users_posts_key,
            'Post': Post,
            'MyUser': MyUser
        }

        template = JINJA_ENVIRONMENT.get_template('timeline.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # GET USER KEY
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())



