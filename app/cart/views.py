from flask import url_for, abort, render_template, redirect, flash, request, session
from flask_login import login_required, current_user
from . import cart_blueprint as cart
from app.models import Cart, MenuItem
from sqlalchemy.orm.exc import NoResultFound
from app import db
from sqlalchemy import desc
from sqlalchemy import and_, or_, not_

@cart.route('/cart/add', methods=['GET', 'POST'])
@login_required
def addToCart():
    """
    create shopping cart
    """
    itemId = request.args.get('itemId')
    if itemId is not None:
        try:
            MenuItem.query.filter_by(id=itemId).first()
        except NoResultFound:
            flash("The food does not exist!")
            return redirect('home.index')
        else:
            user_id = current_user.id
            cart_obj = Cart(user=user_id, menuItem_id=itemId)
            # add cart to database
            db.session.add(cart_obj)
            db.session.commit()
            session['cart'] = {'id':cart_obj.id, 'user':cart_obj.user, 'menuItem_id':cart_obj.menuItem_id}
        return_url = request.referrer or '/'
        return redirect(url_for('cart.Home'))

@cart.route('/cart/index', methods=['GET', 'POST'])
@login_required
def Home():
    """
    display current logined user's shopping cart
    """
    cart_id = request.args.get('cid')
    user_id = current_user.id
    cart_items = Cart.query.filter(and_(Cart.user == user_id, Cart.status == 0)).order_by(Cart.created_on.asc())

    query = db.session().query(Cart, MenuItem)
    query = query.join(MenuItem, Cart.menuItem_id == MenuItem.id)\
        .filter(and_(Cart.user == user_id, Cart.status == 0)).order_by(Cart.created_on.asc())

    # for m in query.all():
    #     print(type(m.MenuItem))
    total_price=0
    cart_menu_items=[]
    for m in query.all():
        cart_menu_items.append(m.MenuItem)
        total_price+=m.MenuItem.price

    num_cart_items = cart_items.count()
    # print('num_cart_items', num_cart_items)
    session['num_cart_items'] = num_cart_items
    return render_template('cart/cart_home.html', cart_menu_items=cart_menu_items,
                           num_cart_items=num_cart_items, total_price=total_price)