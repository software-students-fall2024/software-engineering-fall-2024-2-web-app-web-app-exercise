import flask_login
from src.app import login_manager

class User(flask_login.UserMixin):
    pass

users = {'username': {'password': 'password'}}

@login_manager.user_loader
def user_loader(username): 
    print(username)
    if username not in users:
        print("err")
        return
    user = User()
    user.id = username
    return user
@login_manager.request_loader
def request_loader(request):
    email = request.form.get('username')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

