import webapp2
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import cgi
from handlers import *
from utils import *
from models import *



class MainPage(webapp2.RequestHandler):
    def get(self):
        user=get_current_user(self)
        if user:
            self.redirect('/home') 
        self.response.out.write(template.render("templates/landingpage.html",locals()))
        
class Home(webapp2.RequestHandler):
    def get(self):
        user=get_current_user(self)
        if user:
            self.response.out.write(template.render("templates/home.html",locals()))
        else:
            self.redirect('/')
        
        
class ViewQuestions(webapp2.RequestHandler):
    def get(self):
        user=get_current_user(self)
        if user:    
            status = True
        else:
            status = False
        tags=Tag.all()
        self.response.out.write(template.render("templates/view.html",locals()))

    def post(self):
        user=get_current_user(self)
        if user:   
            status = True
        else:
            status = False
        tags=Tag.all()
        tag=self.request.get('tag')
        q = Question.all()
        questions=q.filter("tags =", tag)
        if not user:
            questions=questions.fetch(10)
        self.response.out.write(template.render("templates/view.html",locals()))

class CreateCategory(webapp2.RequestHandler):
    def get(self):
        user=get_current_user(self)
        
        if user:
            tags=Tag.all()
            self.response.out.write(template.render("templates/tags.html",locals()))
        else:
            self.redirect('/')
            

    def post(self):
        user=get_current_user(self)
        if user:
            new_tag=self.request.get('newtag')                        
            query=Tag.all()
            query.filter("tag =", new_tag)
            q=query.get()
            if q is not None:
                message='Tag already Exists!'
                tags=Tag.all()
                self.response.out.write(template.render("templates/tags.html",locals()))
            else:
                tag=Tag(tag=new_tag)
                tag.put()
                message='Tag added!'
                tags=Tag.all()
                self.response.out.write(template.render("templates/tags.html",locals()))
        else:
            self.redirect('/')
            
            
class CreateQuestion(webapp2.RequestHandler):
    def get(self):
        user=get_current_user(self)
        
        if user:
            tags=Tag.all()
            message = 'Please create a Question'
            self.response.out.write(template.render("templates/index.html", locals()))
                
        else:
            self.redirect('/')
    
    def post(self):
        user=get_current_user(self)
        
        if user:
            new_question=self.request.get('question')
            tag=self.request.get('tag')
            question=Question(content=new_question,tags=tag)
            question.put()
            tags=Tag.all()
            message= 'Question Added! Add more!'
            self.response.out.write(template.render("templates/index.html",locals()))
        else:
            self.redirect('/')
        

app = webapp2.WSGIApplication([('/', MainPage),('/home',Home),
                              ('/view-questions', ViewQuestions),('/create-questions', CreateQuestion),('/add-category',CreateCategory),('/login',Login),
                               ('/register',Register),('/logout',Logout)],
                              debug=True)
