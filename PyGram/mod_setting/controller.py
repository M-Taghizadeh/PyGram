from . import setting
from PyGram.utils.check_auth import check_user_auth
from flask import render_template, request
from PyGram.models import User
from PyGram import db
from PyGram.utils.upload import upload_file

@setting.route("/<string:username>", methods=["GET", "POST"])
def setting_index(username):

    # Check User Auth
    if check_user_auth(username):
        # Upload User Avatar:
        if request.method == "POST":  
            this_file = request.files.get("filename") # Get File
            # Check file :
            if this_file:
                avatar_path = upload_file(this_file, username)
                user = User.query.filter_by(username = username).first()
                user.avatar = avatar_path
                db.session.commit()

        user = User.query.filter_by(username = username).first()
        avatar = user.avatar 
        return render_template("setting.html", user=user)

    else:
        return "You have not any access to this page."