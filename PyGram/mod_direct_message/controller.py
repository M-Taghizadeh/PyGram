from . import direct
from flask import render_template, session, redirect, url_for, request
from PyGram.utils.check_auth import check_user_auth
from PyGram.models import User, Direct_Message
from PyGram import db
from sqlalchemy import or_

@direct.route("/<string:username>")
def direct_index(username):
    # check user authentication
    if check_user_auth(username):
        user = User.query.filter_by(username=username).first()
        # get all directmessages of this user:
        direct_messages = Direct_Message.query.filter_by(recipient_username = username).order_by(Direct_Message.sending_date.desc()).all()
        return render_template("direct-message.html", user=user, direct_messages=direct_messages)


@direct.route("/chat/<string:username>", methods=["GET"])
def chat(username):
    loged_in_username = session.get("username")
    if check_user_auth(loged_in_username):
        loged_in_user = User.query.filter_by(username=loged_in_username).first()
        user = User.query.filter_by(username=username).first()

        cnd_1 = Direct_Message.query.filter_by(sender_username=loged_in_username, recipient_username=username)
        cnd_2 = Direct_Message.query.filter_by(sender_username=username, recipient_username=loged_in_username)

        ### using or_ SQLAlchemy : by default is and
        messages = cnd_1.union(cnd_2)
        messages = messages.order_by(Direct_Message.sending_date.asc())

        return render_template("single-direct-message.html",messages=messages, user=user, loged_in_user=loged_in_user )


@direct.route("/send_message/<string:username>", methods=["POST"])
def send_message(username):
    loged_in_username = session.get("username")
    if check_user_auth(loged_in_username):
        loged_in_user = User.query.filter_by(username=loged_in_username).first()
        user = User.query.filter_by(username=username).first()
        msg = Direct_Message()
        msg.sender = loged_in_user
        msg.recipient = user
        if request.form.get("message_text"):
            msg.message_text = request.form.get("message_text")
            db.session.add(msg)
            db.session.commit()
            
        return redirect(url_for('direct.chat', username=username))
    

