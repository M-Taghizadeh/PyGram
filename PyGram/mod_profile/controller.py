from . import profile
from flask import render_template, url_for, redirect, session
from PyGram.utils.check_auth import check_user_auth
from PyGram.models import User, Post, Follow, Like
from PyGram import db

@profile.route("/<string:username>")
def profile_index(username):

    # Check User Auth..
    if check_user_auth(username):
        user = User.query.filter_by(username = username).first()
        # Join Follow and post for get post of followers of this user 
        following_cnd = Follow.query.filter_by(follower_username = username).all()
        query = db.session.query(
            Follow,
            Post
        ).filter(
            Follow.follower_username == user.username
        ).filter(
            Follow.following_username == Post.username
        ).order_by(Post.post_date.desc()).all()
        print(query)

        POSTS_INFO = []
        for q in query:
            post_like_number = len(Like.query.filter_by(like_recipient=q.Post.username, post_date=q.Post.post_date).all())
            POSTS_INFO.append({
                "Post": q.Post,
                "Follow" : q.Follow,
                "Likes": post_like_number
            })

        return render_template("profile.html", user=user, POSTS_INFO=POSTS_INFO)
    
    else:
        return "You have not access to this page"


@profile.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for('index'))