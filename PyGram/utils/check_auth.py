# check this user loged in or not 
from flask import session
from PyGram import db
from PyGram.models import User

def check_user_auth(username):
    user = User.query.filter_by(username = username).first()
    session_username = session.get("username")
    session_password = session.get("password")

    # check user 
    if not user:
        return False
    
    # check user activation
    if not user.active:
        return False

    # check username 
    if not user.username == session_username:
        return False

    # check password
    if not user.check_pass(session_password):
        return False

    # every things is ok
    return True