# send activation email (registration and connection to redis)
from PyGram import mail
from flask import url_for
import random
from PyGram import redis

def send_signup_email(user, token):
    url = url_for("signup_process", username=user.username, token=token, _external=True)
    sender = 'taghizadeh.py@gmail.com'
    recipients = [user.email]
    subject = "PyGram Registration Confirm"
    body = f'Hello dear {user.name} {user.lastname}<br>you have registered with {user.username} username<br>activation token is : {token}<br>activation link: {url}'
    mail.send_message(sender=sender, recipients=recipients, subject=subject, html=body)

def create_random_token():
    toekn = random.randint(100000, 999999)
    return toekn

# Redis => [Key Value DataBse] your data have a key for example => 6_register : 12345 [6 is user id mode is register and token
def add_to_redis(username, token, mode):
    key = f'{username}_{mode.lower()}'
    value = token

    # REDIS ADD => key, value, expiry_time(s)
    redis.set(key, value, 3600) 

def get_from_redis(username, mode):
    key = f'{username}_{mode.lower()}'
    return redis.get(key) # get a byte string we must cast to str

def delete_from_redis(username, mode):
    key = f'{username}_{mode.lower()}'
    redis.delete(key)