from flask import Blueprint


bp = Blueprint('service', __name__)


from . import views  # NOQA