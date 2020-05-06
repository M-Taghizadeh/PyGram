from flask import Blueprint

post = Blueprint("post", __name__, url_prefix="/post/")

from . import controller