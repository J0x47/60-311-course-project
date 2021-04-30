from flask import Blueprint

cart_blueprint = Blueprint('cart', __name__)

from . import views