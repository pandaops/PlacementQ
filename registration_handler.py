def handle_registration(self):

# Need to work on this asap.

    username=kwargs.get('username')
    password=kwargs.get('password')
    rpassword=kwargs.get('rpassword')
    firstname=kwargs.get('firstname')
    lastname=kwargs.get('lastname')
    global global_messages
    global_messages =[]
    if password != rpassword:
        global_messages.append("Passwords don't match!")
        allowed =False
        return allowed
    if firstname=='':
        allowed = False
        global_messages.append("Enter a valid First Name")
        return allowed
    if lastname=='':
        allowed = False
        global_messages.append("Enter a valid Last Name")
        return allowed
    if username=='':
        allowed = False
        global_messages.append("Enter a valid Last Name")
        return allowed
    q=User.all()
    q.filter("username =", username)
    q=q.get()
    try:
        if q.username:
            allowed = False
            global_messages.append("Username already exists!")
            return allowed
    except:
        pass
    allowed = True
    return allowed
        


        
