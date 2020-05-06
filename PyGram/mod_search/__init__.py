from flask import Blueprint

search = Blueprint("search", __name__, url_prefix="/search/")

from . import controller