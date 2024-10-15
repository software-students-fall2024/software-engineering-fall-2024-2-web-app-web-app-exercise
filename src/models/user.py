import flask_login
from src.app import login_manager
from flask import session
from src.app import get_db


class User(flask_login.UserMixin):
    pass


def find_user(email: str):
    users = get_db().users
    return users.find_one({"email": email}, {})


def validate_password(email: str, password: str):
    users = get_db().users
    return users.find_one({"password": password, "email": email}, {})


def create_user(email: str, username: str, password: str):
    users = get_db().users
    return users.insert_one({"email": email,
                             "username": username,
                             "password": password,
                             "privacy": "Public",
                             "language": "English (US)",
                             "theme": "light"
                             })


@login_manager.user_loader
def user_loader(email):
    found = find_user(email)  # Fetch user from the database
    if not found:
        return None  # Return None if the user isn't found

    user = User()
    user.id = email
    user.email = email
    user.username = found['username']
    user.privacy = found['privacy']
    user.theme = found['theme']
    user.language = found['language']

    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if not find_user(email):
        return
    user = User()
    user.id = email
    return user
