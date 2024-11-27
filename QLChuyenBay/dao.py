import json, os
from QLChuyenBay import app, db
from QLChuyenBay.models import User, UserRole
import hashlib
import re

def add_user(name, username, password, email, **kwarg):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    user = User(name = name, username = username, password = password,
                email = email, avatar = kwarg.get('avatar'))
    db.session.add(user)
    db.session.commit()

def check_secure_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    if re.match(pattern, password):
        return True

def check_login(username, password, role= UserRole.USER):
    if username and password:
        password= str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

def check_mail_exit(email):
    if email:
        return User.query.filter(User.email.__eq__(email)).first()


def override_password(email, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    user= User.query.filter(User.email.__eq__(email)).first()
    if user:
        user.password= password
        db.session.commit()

def get_user_by_id(user_id):
    return User.query.get(user_id)
