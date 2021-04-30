from flask import url_for, abort, render_template, redirect, flash, request, session
from flask_login import login_required, current_user
from app.models import Reservation, User
from . import order_blueprint
from app import db
from sqlalchemy import and_, or_, not_
from flask_wtf import Form
from wtforms.fields import DateField, DateTimeField
from app.models import Order, OrderDetails

@order_blueprint.route('/orders')
@login_required
def view_orders():
    """
    list all  checked-out order by created time (desc)
    """
    user_id = current_user.id
    cart = session['cart']
    cart_id = cart.id
    # userobj = User.query.filter_by(id=user_id).first()

    all_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_on.desc()).all()

    return render_template('order/orders.html',
                           order_list=all_orders, title="Order List")
