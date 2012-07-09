import email.utils
import hmac
import haslhib
import Cookie
import time
from handlers import *
from models import *

def get_current_user(self):
    if not hasattr(_current_user, selfobject):
        self._current_user=None
        userid = parse_cookie(self)
        if user_id:
            self._current_user = User.get_by_key_name(user_id)
    return self._current_user        
            
        
def parse_cookie(self):
    cookie = self.request.cookies.get('placementq')
    values = cookie.split('|')
    if len(values)!=3:
        return None
    timestamp = int(parts[1])
    if cookie_signature(values[0], values[2]) == values[1]): 
        if timestamp < time.time() - 30 * 86400:
            return None
        try:
            return values[0]
        except:
            return None
    return None           
    
    
def cookie_signature(*_args):
    salthash = hmac.new('salt')
    for arg in _args:
        salthash.update(arg)
        
    return salthash.hexdigest()     
    
 
#name is placementq and value is the UID 
def set_cookie(response, name, value, domain=None, path="/", expires=None):
    timestamp=str(int(time.time()))
    uid = value
    signature = cookie_signature(uid,timestamp)
    cookie = Cookie.BaseCookie()
    cookie[name]="|".join([uid,signature,timestamp])
    cookie[name]["path"]=path
    if domain:
        cookie[name]["domain"]=domain
    if expires:
        cookie[name]["expires"]= email.utils.formatdate(expires,localtime=False, usegmt=True)
    response.headers._headers.append(("Set-Cookie",cookie.output()[12:]))
    

def handle_registration(data):
    username=data.request.get('username')
    password=data.request.get('password')
    rpassword=data.request.get('rpassword')
    firstname=data.request.get('firstname')
    lastname=data.request.get('lastname')
    if authenticate_data(**locals()):
        new_user=User(first_name=firstname,last_name=lastname,username=username,password=password)
        new_user.put()
        set_cookie(self.response, "placementq", str(new_user.uid), expires=time.time() + 30 * 86400)
        return True
    else:
        return False



def authenticate_data(**kwargs):
    username=kwargs.get('username')
    password=kwargs.get('password')
    rpassword=kwargs.get('rpassword')
    firstname=kwargs.get('firstname')
    lastname=kwargs.get('lastname')
    if password != rpassword:
        messages.append("Passwords don't match!")
        allowed =False
        return allowed
    if firstname=='':
        allowed = False
        messages.append("Enter a valid First Name")
        return allowed
    if lastname=='':
        allowed = False
        messages.append("Enter a valid Last Name")
        return allowed
    if username=='':
        allowed = False
        messages.append("Enter a valid Last Name")
        return allowed
    q=User.all()
    q.filter("username =", username)
    q=q.get()
    try:
        if q.username:
            allowed = False
            messages.append("Username already exists!")
            return allowed
    except:
        pass
    allowed = True
    return allowed   
    
    
    
    
    
    
    
    
    
    
    
    
        
