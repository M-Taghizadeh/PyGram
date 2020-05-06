from . import user_page
from PyGram.models import User, Post, Follow
from flask import render_template, session, redirect, url_for
from PyGram.utils.check_auth import check_user_auth
from PyGram import db

@user_page.route("/<string:username>")
def user_page_index(username):
    loged_in_username = session.get("username")
    if loged_in_username:
        loged_in_user = User.query.filter_by(username=loged_in_username).first()
        user = User.query.filter_by(username=username).first()
        posts = Post.query.filter_by(username = username).order_by(Post.post_date.desc()).all()
        follower_number = len(Follow.query.filter_by(following_username=username).all())
        following_number = len(Follow.query.filter_by(follower_username=username).all())
        
        # check this user followed by loged_in_user or not
        result_count = Follow.query.filter_by(follower_username=loged_in_username, following_username=username).count()
        if result_count == 1:
            flag_followed = True
        else:
            flag_followed = False

        return render_template("single-user-page.html", loged_in_user=loged_in_user, user=user, posts=posts, follower_number=follower_number, following_number=following_number, flag_followed=flag_followed)

@user_page.route("/follow-process/<string:username>/")
def follow_process(username):
    loged_in_username = session.get("username")
    if check_user_auth(loged_in_username):
        f = Follow.query.filter_by(follower_username=loged_in_username, following_username=username).first()
        if not f:
            loged_in_user = User.query.filter_by(username=loged_in_username).first()
            user = User.query.filter_by(username=username).first()  
            # FOLLOW
            f = Follow()
            f.follower = loged_in_user
            f.following = user
            db.session.add(f)
            db.session.commit()
            return redirect(url_for("user_page.user_page_index", username=username))

@user_page.route("/unfollow-process/<string:username>/")
def unfollow_process(username):
    loged_in_username = session.get("username")
    if check_user_auth(loged_in_username):
        f = Follow.query.filter_by(follower_username=loged_in_username, following_username=username).first()
        if f:
            user = User.query.filter_by(username=username).first()  
            # UNFOLLOW
            db.session.delete(f)
            db.session.commit()
            return redirect(url_for("user_page.user_page_index", username=username))