from flask import Blueprint


admin_blueprint = Blueprint('admin', __name__)
# admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


from . import views

# __all__ = ['models']