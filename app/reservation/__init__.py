from flask import Blueprint


reservation_blueprint = Blueprint('reservation', __name__)

from . import views