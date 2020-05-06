from flask import Blueprint

direct = Blueprint("direct", __name__, url_prefix="/direct/")

from . import controller