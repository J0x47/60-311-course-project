from flask import Blueprint


order_blueprint = Blueprint('order', __name__)

from . import views