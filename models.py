from google.appengine.ext import db
from google.appengine.api.users import User

class Image(db.Model):
    image = db.BlobProperty()
    thumb = db.BlobProperty()
    original = db.BlobProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    user = db.UserProperty()