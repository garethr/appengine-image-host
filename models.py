from google.appengine.ext import db
from google.appengine.api.users import User

class Image(db.Model):
    "Represents an image stored in the datastore"
    # blog properties storing up to 1MB of binary data
    image = db.BlobProperty()
    thumb = db.BlobProperty()
    original = db.BlobProperty()
    # store the date just in case
    date = db.DateTimeProperty(auto_now_add=True)
    # all images are associated with the user who uploades them
    # this way we can make it a multi user system if that's useful
    user = db.UserProperty()