import os
import datetime

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import Image
  
class GenericServer(webapp.RequestHandler):
    property = 'image'
    def get(self):
        image = db.get(self.request.get("id"))
        if image.image:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(eval("image.%s" % self.property))
        else:
            self.error(404)

class ImageServer(GenericServer):
    property = 'image'

class ThumbServer(GenericServer):
    property = 'thumb'

class OriginalServer(GenericServer):
    property = 'original'

application = webapp.WSGIApplication([
    ('/i/img', ImageServer),
    ('/i/thumb', ThumbServer),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()