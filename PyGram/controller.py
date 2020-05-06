from flask import Flask, render_template, flash, request, redirect, url_for, session
from . import app
from PyGram import db
from PyGram.models import User
from PyGram.utils.registration import send_signup_email, create_random_token, add_to_redis, get_from_redis, delete_from_redis

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        username = request.form.get("username")
        country = request.form.get("country")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if (not name) or (not lastname) or (not email) or (not username) or (not country) or (not password) or (not confirm):
            flash("Please fill all the fields.")
            return redirect(url_for("signup"))
        if not password == confirm:
            flash("Password and password confirmation must be the same.")
            return redirect(url_for("signup"))
        if len(password)<4:
            flash("Password should be atleast 4 characters.")
            return redirect(url_for("signup"))

        # check user is exist or not 
        user = User.query.filter_by(username = username).first()
        if user:
            flash("Username already exists")
            return redirect(url_for("signup"))
        
        # add user to database:
        user = User()
        user.name = name
        user.lastname = lastname
        user.email = email
        user.username = username
        user.country = country
        user.password = password
        db.session.add(user)
        db.session.commit()

        # TOKEN ADD TO REDIS
        token = create_random_token()
        add_to_redis(username, token, "register")
        send_signup_email(user, token)

        return "<h1>Thank's for registration and Welcome to Paygram :)</h1><h4>Please check your email account. We sent you an email to activate your account.</h4>"
    
    return render_template("signup.html")


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username = username).first()
        if not user:
            flash("User not found!")
            return render_template("login.html")
        
        if not user.check_pass(password):
            flash("Password is not correct")
            return render_template("login.html")

        session["username"] = username
        session["password"] = password

        return redirect(url_for("profile.profile_index", username=username))

    if request.method == "GET":
        username = session.get("username")
        password = session.get("password")

        if username and password:
            user = User.query.filter_by(username = username).first()
            if not user:
                flash("User not found!")
                return render_template("login.html")
            
            if not user.check_pass(password):
                flash("Password is not correct")
                return render_template("login.html")

            return redirect(url_for("profile.profile_index", username=username))

    return render_template("login.html")


@app.route("/signup-process/")
def signup_process():
    username = request.args.get("username")
    token = request.args.get("token")

    # user validation
    user = User.query.filter_by(username = username).first()
    if not user:
        return "User not found!"
    
    # token validation
    token_from_redis = get_from_redis(username, "register") # get a byte string we must cast to str
    if not token_from_redis:
        return "Warning! Somethings Wrong or Expired Token."
    if token != token_from_redis.decode("UTF-8"):
        return "Warning! Your token is wrong."

    ### Activation process:
    # 1: Delete token from redis
    delete_from_redis(username, "register")
    user.active = True
    db.session.commit()

    # 2: Set Session : saving 1:username
    session["username"] = username

    # After activation
    # 1: create directory for this user 
    import os
    path = "PyGram/static/upload/" + username
    os.mkdir(path)
    
    # 3: Set Flash message
    flash("Your account has been successfully activated. You can now log in to Paygram")

    # 2:redirect to login page
    return redirect(url_for('login'))
