from flask import Flask, render_template, abort
import flask.globals as flask_global
from config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
import jinja2
from jinja2 import evalcontextfilter, Markup, escape
import os
import re
from flask_sqlalchemy import models_committed
from flask_marshmallow import Marshmallow

flask_bcrypt = None
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

db = SQLAlchemy()
ma = Marshmallow() # object serialization/deserialization library

# after existing third-party imports
from flask_login import LoginManager

# after the db variable initialization
login_manager = LoginManager()

# it works in here
# @models_committed.connect
# def on_models_committed_1(sender, changes):
#     print('on_models_committed_1')
#     print(changes)
def on_models_committed(sender, changes):
    print 'I subscript the signal'
    for obj, change in changes:
        if change == 'insert' and hasattr(obj, '__commit_insert__'):
            print("receive signal?")
            obj.__commit_insert__()
        elif change == 'update' and hasattr(obj, '__commit_update__'):
            print("update")
        elif change == 'delete' and hasattr(obj, '__commit_delete__'):
            pass

models_committed.connect(on_models_committed)


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])  # Configure app according to the environment
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")),])
    app.jinja_loader = my_loader

    global flask_bcrypt
    flask_bcrypt = Bcrypt(app)
    Bootstrap(app)
    db.init_app(app)

    # login_manager from flask-login extension
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    Migrate(app, db)
    # from app import models
    import models
    ma.init_app(app) # initialize with app

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .admin import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .home import home_blueprint
    app.register_blueprint(home_blueprint)

    from .menu import menu_blueprint
    app.register_blueprint(menu_blueprint)

    from .cart import cart_blueprint
    app.register_blueprint(cart_blueprint)

    from .order import order_blueprint
    app.register_blueprint(order_blueprint)

    from .reservation import reservation_blueprint
    app.register_blueprint(reservation_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500


    # This is a nl2br (newline to <BR>) filter
    # from http://flask.pocoo.org/snippets/28/
    @app.template_filter()
    @evalcontextfilter
    def nl2br(eval_ctx, value):
        result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
            for p in _paragraph_re.split(escape(value)))
        if eval_ctx.autoescape:
            result = Markup(result)
        return result

    # @models_committed.connect
    # def on_models_committed_1(sender, changes):
    #     print('on_models_committed_1')
    #     print(changes)

    # https://stackoverflow.com/questions/33848862/flask-login-how-to-set-blueprint-login-views-to-have-blueprint-specific-login
    # login_manager.blueprint_login_views = {
    # 'home': 'auth.login',
    # 'admin' : 'admin.login',
    # }


    return app


