from flask import Blueprint

follow = Blueprint("follow", __name__, url_prefix="/follow/")

from . import controller