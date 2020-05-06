from flask import Flask
from .config import Development
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from redis import Redis

app = Flask(__name__)
app.config.from_object(Development)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
redis = Redis.from_url(app.config["REDIS_SERVER_URL"])

# import models
from . import models

# import controller
from . import controller

# import blueprints : 
from .mod_profile import profile
from .mod_post import post
from .mod_setting import setting
from .mod_search import search
from .mod_user_page import user_page
from .mod_direct_message import direct
from .mod_follow import follow

# register blueprints :
app.register_blueprint(profile)
app.register_blueprint(post)
app.register_blueprint(setting)
app.register_blueprint(search)
app.register_blueprint(direct)
app.register_blueprint(user_page)
app.register_blueprint(follow)
