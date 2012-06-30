from google.appengine.ext.webapp import template
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db
import hashlib
from handlers import *


def login(webapp2.RequestHandler):
    def get(self):
        get_current_user(self)
        if self._current_user:
            return self._current_user
        else:
            self.redirect('/')
            
    def post(self):
        username=self.request.get('username')
        password=self.request.get('password')
        user = UserProfile.all()
        user.filter("username =", username)
        user.get()
        hash_password=hashlib.new()
        if hash_password.update(password).hexdigest() == user.password:
            set_cookie(self.response, "placementq", str(user.uid), expires=time.time() + 30 * 86400)
            self.redirect('/home')
        else:
            self.redirect('/')
            
            
def logout(webapp2.RequestHandler):
    def get(self):
        set_cookie(self.response, "placementq", "", expires=time.time() - 30 * 86400)
        self.redirect('/')
        
        
def register(webapp2.RequestHandler):
    def get(self):
        get_current_user(self)
        if self._current_user:
            self.redirect('/home')
    
    def post(self):
        success = handle_registration(self)
        if success:
            self.redirect('/home')
        else:
            self.redirect('/')    
        
            
         
            
    
