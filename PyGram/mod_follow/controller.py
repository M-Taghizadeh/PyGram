from . import follow
from PyGram.utils.check_auth import check_user_auth
from PyGram.models import User, Follow
from flask import render_template

@follow.route("/<string:username>")
def follow_index(username):
    if check_user_auth(username):
        user = User.query.filter_by(username=username).first()
        followers = Follow.query.filter_by(following_username=username).all()
        followings = Follow.query.filter_by(follower_username=username).all()

        return render_template("follower-following.html", user=user, followers=followers, followings=followings)