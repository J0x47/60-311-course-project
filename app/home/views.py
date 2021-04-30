from flask import request, render_template
# from app.custom_http_respones.responses import Success, Error
# from app.decorators.decorators import token_required, admin_only
# from flask_login_multi import login_required,current_user, login_required, logout_user

from flask_login import login_required, login_required,current_user, login_required, logout_user
from . import home_blueprint as home
from app.models import User
from app.models import MenuItem, Cart
from sqlalchemy import and_, or_, not_
from sqlalchemy import desc, asc

@home.route('/')
def index():
    menu_items = MenuItem.query.filter_by(is_featured=True).all()
    cart_obects = Cart
    # latest_cart_item = Cart.query.filter(and_(Cart.user == current_user.id, Cart.status == 0)).order_by(Cart.created_on.desc()).first()
    # print(latest_cart_item.id)
    return render_template('home/index.html',
                           object_list=menu_items, cart=cart_obects, title="Fresh Food")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    latest_cart_item = Cart.query.filter(and_(Cart.user == current_user.id, Cart.status == 0)).order_by(Cart.updated_on.desc()).first()
    # print(latest_cart_item.id)

    return render_template('home/dashboard.html', title="Dashboard")

