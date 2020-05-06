from . import db
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates, relationship
import datetime as dt 

# Entities => 1:User, 2:Post, 3:Follow, 4:Comment, 5:Like, 6:Direct_Message]

class User(db.Model):
    __tablename__ = "users"

    name = Column(String(32), nullable = False)
    lastname = Column(String(32), nullable = False)
    email = Column(String(256), nullable = False)
    username = Column(String(64), primary_key = True)
    country = Column(String(32), nullable = False)
    password = Column(String(128), nullable = False)
    avatar = Column(String(256), nullable = False, default = "/static/upload/avatar.png")
    active = Column(Boolean, nullable = False, default = False)

    # list of posts
    posts = relationship("Post", backref="user")

    # list of follows
    followers = relationship("Follow", backref="follower", foreign_keys='Follow.follower_username')
    following = relationship("Follow", backref="following", foreign_keys='Follow.following_username')

    # list of comments
    cm_senders = relationship("Comment", backref="sender", foreign_keys='Comment.cm_sender')
    cm_recipients = relationship("Comment", backref="recipient", foreign_keys='Comment.cm_recipient')

    # list of likes
    like_sender = relationship("Like", backref="sender", foreign_keys='Like.like_sender')
    like_recipient = relationship("Like", backref="recipient", foreign_keys='Like.like_recipient')

    # list of direct_messages
    direct_senders = relationship("Direct_Message", backref="sender", foreign_keys='Direct_Message.sender_username')
    direct_recipients = relationship("Direct_Message", backref="recipient", foreign_keys='Direct_Message.recipient_username')

    
    # Validation on fields
    @validates('username')
    def validates_username(self, key, value):
        if not value.isidentifier():
            raise ValueError("username is invalid")

        if len(value)<3:
            raise ValueError("username should be atleast 3 characters.") 
        return value
        
    @validates('password')
    def validates_password(self, key, value):  
        if len(value)<4:
            raise ValueError("password should be atleast 4 characters.") # raise for return error (bad request)
        return generate_password_hash(value) # return by default set thit value to our field :)

    # Methods
    def check_pass(self, password):
        return check_password_hash(self.password, password) ### return a boolean 


class Post(db.Model):
    __tablename__ = "posts"
    username = Column(String(64), ForeignKey('users.username'), primary_key = True)
    caption = Column(Text(), nullable = True)
    picture = Column(String(256), nullable = False)
    post_date = Column(DateTime(), default = dt.datetime.utcnow, primary_key = True)


class Follow(db.Model):
    __tablename__ = "follows"
    follower_username = Column(String(64), ForeignKey('users.username'), primary_key = True)
    following_username = Column(String(64), ForeignKey('users.username'), primary_key = True)


class Comment(db.Model):
    __tablename__ = "comments"
    cm_sender = Column(String(64), ForeignKey('users.username'), primary_key = True)
    cm_recipient = Column(String(64), ForeignKey('users.username'))
    post_date = Column(DateTime(), nullable=False)
    text = Column(Text(), nullable = False)
    comment_date = Column(DateTime(), default = dt.datetime.utcnow, primary_key = True)


class Like(db.Model):
    __tablename__ = "likes"
    like_sender = Column(String(64), ForeignKey('users.username'), primary_key = True)
    like_recipient = Column(String(64), ForeignKey('users.username'))
    post_date = Column(DateTime(), nullable=False)
    like_date = Column(DateTime(), default = dt.datetime.utcnow, primary_key = True)


class Direct_Message(db.Model):
    __tablename__ = "direct_messages"
    sender_username = Column(String(64), ForeignKey('users.username'), primary_key = True)
    recipient_username = Column(String(64), ForeignKey('users.username'), primary_key = True)
    message_text = Column(Text(), nullable = False)
    sending_date = Column(DateTime(), default = dt.datetime.utcnow, primary_key = True)

