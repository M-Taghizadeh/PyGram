from . import search
from PyGram.models import User
from flask_sqlalchemy import get_debug_queries ### for see what query send to or db
from sqlalchemy import or_ ### by default is and
from flask import render_template, request, session
from PyGram.utils.check_auth import check_user_auth

@search.route("/search/")
def search():
    loged_in_username = session.get("username")
    if check_user_auth(loged_in_username):
        q = request.args.get("q")
        name_cnd = User.name.ilike(f'%{q}%')
        lastname_cnd = User.lastname.ilike(f'%{q}%')
        username_cnd = User.username.ilike(f'%{q}%')

        ### using or_ SQLAlchemy : by default is and
        # before pagination
        # found_users = User.query.filter(or_(
        #     name_cnd,
        #     lastname_cnd,
        #     username_cnd
        # )).all()

        # pagination
        p = request.args.get("p", default=1, type=int)
        found_users = User.query.filter(or_(
            name_cnd,
            lastname_cnd,
            username_cnd
        )).paginate(p, 5)
        

        print(found_users)
        print(get_debug_queries()) ### show queries that was sent to database
        loged_in_user = User.query.filter_by(username=loged_in_username).first()
        return render_template("search.html", loged_in_user=loged_in_user, users=found_users, q=q)