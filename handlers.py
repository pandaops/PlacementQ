from google.appengine.ext.webapp import template
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db
import hashlib
from utils import *


def login(webapp2.RequestHandler):
    def get(self):
        user=get_current_user(self)
        if user:
            self.redirect('/home')
        self.redirect('/')
        
            
    def post(self):
        user=get_current_user(self)
        if not user:
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
            self.redirect('/home')               
            
def logout(webapp2.RequestHandler):
    def get(self):
        set_cookie(self.response, "placementq", "", expires=time.time() - 30 * 86400)
        self.redirect('/')
        
        
def register(webapp2.RequestHandler):
    def get(self):
        user=get_current_user(self)
        if user:
            self.redirect('/home')    
        self.response.out.write(template.render("templates/register.html", None))
    
    def post(self):
        user=get_current_user(self)
        if not user:    
            success = handle_registration(self)
            if success:
                self.redirect('/home')
            else:
                self.redirect('/')
        else:
            self.redirect('/home')   
            



        

                
         
            
    
