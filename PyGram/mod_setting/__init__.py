from flask import Blueprint

setting = Blueprint("setting", __name__, url_prefix="/setting/")

from . import controller