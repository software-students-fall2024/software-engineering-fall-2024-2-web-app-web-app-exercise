import flask_login
from src.app import login_manager
from flask import session
from src.app import get_db

class User(flask_login.UserMixin):
   pass


def find_user(email:str, username:str, password:str):
    users = getdb().users
    return users.find_one({"username":username,"email": email}, {})

#def validate_password(email:str, password:str)

users = {'username': {'password': 'password'}}

@login_manager.user_loader
def user_loader(username): 
    if username not in users:
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

