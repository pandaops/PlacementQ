import webapp2
from google.appengine.ext import db
from google.appengine.ext.webapp import template


class Question(db.Model):
    content=db.StringProperty(multiline=True)
    tags=db.StringProperty()

class Tag(db.Model):
    tag=db.StringProperty()

class User(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    username = db.StringProperty()
    password = db.StringProperty()
    
class SessionsTable(db.Model):
    userid = db.StringProperty()
    
    #not using sessions tables as of yet.
    

