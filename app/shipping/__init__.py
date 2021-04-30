from flask import Blueprint


shipping_blueprint = Blueprint('shipping', __name__)

from . import views