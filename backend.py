"""
Provides a protected administrative area for uploading and deleteing images
"""

import os
import datetime

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import images
from google.appengine.ext.webapp import template
from google.appengine.api import users

from models import Image

class Index(webapp.RequestHandler):
    """
    Main view for the application.
    Protected to logged in users only.
    """
    def get(self):
        "Responds to GET requets with the admin interface"
        # query the datastore for images owned by
        # the current user. You can't see anyone elses images
        # in the admin
        images = Image.all()
        images.filter("user =", users.get_current_user())
        images.order("-date")

        # we are enforcing loggins so we know we have a user
        user = users.get_current_user()
        # we need the logout url for the frontend
        logout = users.create_logout_url("/")

        # prepare the context for the template
        context = {
            "images": images,
            "logout": logout,
        }
        # calculate the template path
        path = os.path.join(os.path.dirname(__file__), 'templates',
            'index.html')
        # render the template with the provided context
        self.response.out.write(template.render(path, context))

class Deleter(webapp.RequestHandler):
    "Deals with deleting images"
    def post(self):
        "Delete a given image"
        # we get the user as you can only delete your own images
        user = users.get_current_user()
        key = self.request.get("key")
        if key:
            image = db.get(key)
            # check that we own this image
            if image.user == user:
                image.delete()
        # whatever happens rediect back to the main admin view
        self.redirect('/')
       
class Uploader(webapp.RequestHandler):
    "Deals with uploading new images to the datastore"
    def post(self):
        "Upload via a multitype POST message"
        
        img = self.request.get("img")

        # if we don't have image data we'll quit now
        if not img:
            self.redirect('/')
            return 
            
        # we have image data
        try:
            # check we have numerical width and height values
            width = int(self.request.get("width"))
            height = int(self.request.get("height"))
        except ValueError:
            # if we don't have valid width and height values
            # then just use the original image
            image_content = img
        else:
            # if we have valid width and height values
            # then resize according to those values
            image_content = images.resize(img, width, height)
        
        # get the image data from the form
        original_content = img
        # always generate a thumbnail for use on the admin page
        thumb_content = images.resize(img, 100, 100)
        
        # create the image object
        image = Image()
        # and set the properties to the relevant values
        image.image = db.Blob(image_content)
        # we always store the original here in case of errors
        # although it's currently not exposed via the frontend
        image.original = db.Blob(original_content)
        image.thumb = db.Blob(thumb_content)
        image.user = users.get_current_user()
                
        # store the image in the datasore
        image.put()
        # and redirect back to the admin page
        self.redirect('/')
                
# wire up the views
application = webapp.WSGIApplication([
    ('/', Index),
    ('/upload', Uploader),
    ('/delete', Deleter)
], debug=True)

def main():
    "Run the application"
    run_wsgi_app(application)

if __name__ == '__main__':
    main()