from flask import url_for, render_template, redirect, flash, session
from flask_login import login_user
from flask_login import login_required, login_required,current_user, login_required, logout_user

from . import auth_blueprint as auth

from forms import LoginForm, RegistrationForm
from app import db
from app.models import User

from flask import g
from app.models import Cart, cart_schema, carts_schema
from sqlalchemy import and_, or_, not_
from sqlalchemy import desc, asc
from flask import jsonify


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data,
                            username=form.username.data)

        # add employee to the database
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        # customer = Customer.query.filter_by(email=form.email.data).first()
        user = User.query.filter_by(username=form.username.data).first()
        # print(user)

        if user is not None and user.verify_password(
                form.password.data):
            # log employee in
            login_user(user)

            # redirect to the dashboard page after login
            # return redirect(url_for('home.dashboard'))
             # redirect to the appropriate dashboard page
            if user.is_admin:
                return redirect(url_for('admin.admin_dashboard'))
            else:
                cart = Cart.query.filter(and_(Cart.user == current_user.id, Cart.status == 0)).order_by(Cart.created_on.desc()).first()
                print('>>>>c:', cart)
                if cart is not None:
                    session['cart'] = {'id':cart.id, 'user':cart.user, 'menuItem_id':cart.menuItem_id}
                else:
                    session['cart'] = None
                return redirect(url_for('home.index'))

        # when login details are incorrect
        else:
            flash('Invalid username or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))