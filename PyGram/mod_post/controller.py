from . import post
from flask import render_template, request, session, redirect, url_for
from PyGram import db
from PyGram.models import User, Post, Comment, Like, Follow
from PyGram.utils.check_auth import check_user_auth
from PyGram.utils.upload import upload_file

@post.route("/<string:username>")
def post_index(username):

    # Check user authentication
    if check_user_auth(username):
        # get all posts of this user:
        user = User.query.filter_by(username = username).first()
        posts = Post.query.filter_by(username = username).order_by(Post.post_date.desc()).all()
        follower_number = len(Follow.query.filter_by(following_username=username).all())
        following_number = len(Follow.query.filter_by(follower_username=username).all())
        return render_template("post.html", user = user, posts = posts, follower_number=follower_number, following_number=following_number)
    
    else:
        return "You have not any access to this page"


@post.route("/new/<string:username>", methods=["GET", "POST"])
def new_post(username):
    # Check user authentication
        if check_user_auth(username):
            user = User.query.filter_by(username = username).first()
            # check method of request
            if request.method == "POST":
                # get all posts of this user:
                posts = Post.query.filter_by(username = username).order_by(Post.post_date.desc()).all()

                # create new post
                post = Post()
                caption = request.form.get("caption")
                post.user = user
                post.caption = caption
                # upload post picture
                this_file = request.files.get("picture")
                post.picture = upload_file(this_file, username)

                db.session.add(post)
                db.session.commit()

                return redirect(url_for("post.post_index", username=username))

            if request.method == "GET":
                return render_template("new-post.html", user=user)

        else:
            return "You have not any access to this page"


@post.route("/delete/<string:username>/<string:date>")
def delete_post(username, date):

    if check_user_auth(username):
        post = Post.query.filter_by(username=username, post_date=date).first()
        db.session.delete(post)
        db.session.commit()
    
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(username=username)
    return redirect(url_for("post.post_index", username=username))
    

@post.route("/single/<string:username>/<string:date>")
def single_post(username, date):

    # if user loged_in:
    loged_in_user_username = session.get("username")
    if loged_in_user_username:
        loged_in_user = User.query.filter_by(username=loged_in_user_username).first()
        user = User.query.filter_by(username=username).first()
        this_post = Post.query.filter_by(username=username, post_date=date).first()
        comments = Comment.query.filter_by(cm_recipient=username, post_date=date)
        likes = len(Like.query.filter_by(like_recipient=username, post_date=date).all())
        return render_template("single-post.html", loged_in_user=loged_in_user, user=user, post=this_post, comments=comments, likes=likes)
    else:
        return render_template("login.html")


@post.route("/comment/<string:username>/<string:date>", methods=["POST"])
def comment(username, date):
    # if user loged_in:
    loged_in_user_username = session.get("username")
    if loged_in_user_username:
        loged_in_user = User.query.filter_by(username=loged_in_user_username).first()
        user = User.query.filter_by(username=username).first()
        this_post = Post.query.filter_by(username=username, post_date=date).first()

        # ADD A COMMENT
        if request.form.get("cm_text"):
            cm = Comment()
            cm.sender = loged_in_user
            cm.recipient = user
            cm.post_date = date
            cm.text = request.form.get("cm_text")

            db.session.add(cm)
            db.session.commit()

            return redirect(url_for("post.single_post", username=username, date=date))
    else:
        return render_template("single-post.html", loged_in_user=loged_in_user, user=user, post=this_post)


@post.route("/like/<string:username>/<string:date>")
def like(username, date):
     # if user loged_in:
    loged_in_user_username = session.get("username")
    if loged_in_user_username:
        loged_in_user = User.query.filter_by(username=loged_in_user_username).first()
        user = User.query.filter_by(username=username).first()
        this_post = Post.query.filter_by(username=username, post_date=date).first()

        # ADD A LIKE
        # if user dont like this post before:
        check_like_thst_before = len(Like.query.filter_by(like_sender=loged_in_user_username, like_recipient=username, post_date=date).all())
        if check_like_thst_before == 0:
            like = Like()
            like.sender = loged_in_user
            like.recipient = user
            like.post_date = date

            db.session.add(like)
            db.session.commit()

        return redirect(url_for("post.single_post", username=username, date=date))
    else:
        return render_template("single-post.html", loged_in_user=loged_in_user, user=user, post=this_post)