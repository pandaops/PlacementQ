import webapp2
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import cgi

global_messages = []
current_user = None
def loggedin():
    if current_user is not None:
        return True
    return False
    
class Login(webapp2.RequestHandler):
    def get(self):
        logged_in=loggedin()
        user = current_user
        if logged_in:
            self.redirect('/home')
        self.redirect('/')

    def post(self):
        username=self.request.get('username')
        password=self.request.get('password')
        q=User.all()
        q.filter("username =", username)
        q = q.get()
        if q is not None:
            if q.password == password:
                global current_user
                current_user=q.username
                self.redirect('/home')
        messages = ['Username/Password Incorrect']
        self.response.out.write(template.render("templates/landingpage.html", locals()))

class Register(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render("templates/register.html", None))

    def post(self):
        username=self.request.get('username')
        password=self.request.get('password')
        rpassword=self.request.get('rpassword')
        firstname=self.request.get('firstname')
        lastname=self.request.get('lastname')
        if authenticate(**locals()):
            new_user=User(first_name=firstname,last_name=lastname,username=username,password=password)
            new_user.put()
            global current_user
            current_user=username
            self.redirect('/home')
        else:
            global global_messages
            messages = global_messages
            global_messages =[]
            self.response.out.write(template.render("templates/register.html",locals()))

class Logout(webapp2.RequestHandler):
    def get(self):
        logged_in=loggedin()
        if logged_in:
            global current_user
            current_user= None
            global global_messages
            global_messages=[]
            global_messages.append("You have successfully logged out")
            template_values={'messages':global_messages}
            self.redirect('/')
        else:
            self.redirect('/')
                


class MainPage(webapp2.RequestHandler):
    def get(self):
        logged_in=loggedin()
        user = current_user
        self.response.out.write(template.render("templates/landingpage.html",locals()))
        
class Home(webapp2.RequestHandler):
    def get(self):
        logged_in=loggedin()
        if logged_in:
            user = current_user
            self.response.out.write(template.render("templates/home.html",locals()))
        else:
            self.redirect('/')
        
        
class ViewQuestions(webapp2.RequestHandler):
    def get(self):
        logged_in=loggedin()
        if logged_in:
            user=current_user    
            status = True
        else:
            status = False
        tags=Tag.all()
        self.response.out.write(template.render("templates/view.html",locals()))

    def post(self):
        logged_in=loggedin()
        if logged_in:
            user=current_user    
            status = True
        else:
            status = False
        tags=Tag.all()
        tag=self.request.get('tag')
        q = Question.all()
        questions=q.filter("tags =", tag)
        if not logged_in:
            questions=questions.fetch(10)
        self.response.out.write(template.render("templates/view.html",locals()))

class CreateCategory(webapp2.RequestHandler):
    def get(self):
        logged_in=loggedin()
        user = current_user
        if logged_in:
            tags=Tag.all()
            self.response.out.write(template.render("templates/tags.html",locals()))
        else:
            self.redirect('/')
            

    def post(self):
        logged_in=loggedin()
        user = current_user
        if logged_in:
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
        logged_in=loggedin()
        user = current_user
        if logged_in:
            tags=Tag.all()
            message = 'Please create a Question'
            self.response.out.write(template.render("templates/index.html", locals()))
                
        else:
            self.redirect('/')
    
    def post(self):
        logged_in=loggedin()
        user = current_user
        if logged_in:
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
