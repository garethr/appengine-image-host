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
    def get(self):
        self.response.out.write('<html><body>')

        images = Image.all()
        images.filter("user =", users.get_current_user())
        images.order("-date")

        user = users.get_current_user()
        logout = users.create_logout_url("/")
        
        context = {
            "images": images,
            "logout": logout,
        }
        # calculate the template path
        path = os.path.join(os.path.dirname(__file__), 'templates',
            'index.html')
        # render the template with the provided context
        self.response.out.write(template.render(path, context))
       
class Uploader(webapp.RequestHandler):
    def post(self):
        image = Image()
        original_content = self.request.get("img")
        
        try:
            width = int(self.request.get("width"))
            height = int(self.request.get("height"))
        except ValueError:
            image_content = self.request.get("img")
        else:
            image_content = images.resize(self.request.get("img"), width, height)
        
        thumb_content = images.resize(self.request.get("img"), 100, 100)
        image.image = db.Blob(image_content)
        image.original = db.Blob(original_content)
        image.thumb = db.Blob(thumb_content)
        image.user = users.get_current_user()
                
        image.put()
        self.redirect('/')
                
application = webapp.WSGIApplication([
    ('/', Index),
    ('/upload', Uploader)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()