from flask import Blueprint

user_page = Blueprint("user_page", __name__, url_prefix="/user_page/")

from .import controller