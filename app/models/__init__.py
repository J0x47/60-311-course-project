from flask import current_app
from datetime import datetime, timedelta
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin

from app import db, login_manager
# from app.admin.models import Employee
from flask_bcrypt import Bcrypt
# from app import flask_bcrypt
flask_bcrypt = Bcrypt()
from sqlalchemy import text
# import app
from sqlalchemy import desc
from sqlalchemy import and_, or_, not_
from app import ma


ORDER_STATUS = (
        ('created', 0),
        ('in_process', 1),
        ('paid', 2),
        ('shipped', 3),
        ('refunded', 4),
        ('done', 5),
        ('cancelled', 6),
        ('deleted', 7)  # mark deleted but does not delete an order record from the database
)

CART_STATUS = (
        ('in_cart', 0),
        ('done', 1)
)


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column('Id', db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False, default='')
    username = db.Column(db.String(60), index=True, unique=True)
    last_name = db.Column(db.String(40), nullable=False, default='')
    _password = db.Column('password', db.String(128))
    address = db.Column(db.String(60))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(40), unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, server_default=text('0'))
    is_employee = db.Column(db.Boolean, server_default=text('0'))
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime,  default=datetime.now, onupdate=datetime.now)


    def get_fullname(self):
        return self.first_name + ' ' + self.last_name

    @hybrid_property
    def password(self):
        return self._password


    @password.setter
    def password(self, plaintext):
        self._password = flask_bcrypt.generate_password_hash(plaintext, 12)

    def verify_password(self, plaintext):
        if flask_bcrypt.check_password_hash(self._password, plaintext):
            return True

        return False

    def __repr__(self):
        return '<User: {}>'.format(self.username)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Order(db.Model):
    """This is a model that holds all orders"""

    __tablename__ = 'order'

    id = db.Column('Id', db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.Id'))
    shipping_address = db.Column(db.ForeignKey('shipping.Id'))
    shipping_total = db.Column(db.Numeric(10,2), server_default=text('0.00'))
    order_type = db.Column(db.Integer)
    status = db.Column(db.SMALLINT)
    created_on = db.Column(db.DateTime,default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)

class OrderDetails(db.Model):
    """ This is a model that holds all details related to an order"""
    id = db.Column('Id', db.Integer, primary_key=True)
    order_id = db.Column(db.ForeignKey('order.Id'))
    cart_id = db.Column(db.ForeignKey('cart.Id'))
    menuItem_id = db.Column(db.ForeignKey('menu_item.Id'))
    item_quantity = db.Column(db.Integer)
    item_price = db.Column(db.Numeric(10,2), server_default=text('0.00'))
    subtotal = db.Column(db.Numeric(10,2), server_default=text('0.00'))
    total = db.Column(db.Numeric(10,2), server_default=text('0.00'))
    status = db.Column(db.SMALLINT)
    created_on = db.Column(db.DateTime,default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)


class Shipping(db.Model):
    """This is a model that holds all shipping info."""

    __tablename__ = 'shipping'

    id = db.Column('Id', db.Integer, primary_key=True)
    user = db.Column(db.ForeignKey('user.Id'))
    name = db.Column(db.String(50), nullable=False)
    address_line1 = db.Column(db.String(120), nullable=False)
    address_line2 = db.Column(db.String(120))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50), default='Canada')
    postal_code = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)


class MenuCategory(db.Model):
    """This is model to holld all menu categories"""
    __tablename__ = 'menu_category'

    id = db.Column('Id', db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)


class MenuItem(db.Model):
    """This is a model to hold all the menu items"""

    __tablename__ = 'menu_item'

    id = db.Column('Id', db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Numeric(10,2), server_default='0.00')
    desc = db.Column(db.Text)
    image = db.Column(db.String(40))
    cat_id = db.Column(db.Integer, db.ForeignKey('menu_category.Id'), index = True)
    discount = db.Column(db.Numeric(5,2), server_default='0.00')
    is_featured = db.Column(db.Boolean, server_default=text('0'))

    def __repr__(self):
        return '<MenuItem: id:{}, name:{}, price:{},c:{}>'.format(
            self.id, self.name, self.price, self.is_featured)



class Cart(db.Model):
    """This is a model to hold all the menu items"""

    __tablename__ = 'cart'


    id = db.Column('Id', db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.Id'))
    menuItem_id = db.Column(db.Integer, db.ForeignKey('menu_item.Id'))
    subTotal = db.Column(db.Numeric(10, 2), server_default='0.00')
    total = db.Column(db.Numeric(10, 2), server_default='0.00')
    status = db.Column(db.SMALLINT, server_default=text('0'))
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime,  default=datetime.now, onupdate=datetime.now)

    def cart_is_not_empty(self):
        return Cart.query.filter_by(and_(Cart.user == self.user, Cart.menuItem_id == self.menuItem_id)).count > 0

    def __commit_insert__(self):
        # Do Stuff , this will execute after each insert on this table
        print("Cart: insertion", self.id)
    def __commit_update__(self):
       # Do Stuff , this will execute after each update on this table
        pass

class Table(db.Model):

    __tablename__ = 'table'

    # dict(tuple).get('key')
    TABLE_STATUS = (
    ('not_occupied', 0),
    ('occupied', 1)
    )

    id = db.Column('Id', db.Integer, primary_key=True)
    size = db.Column(db.Integer, nullable=False)
    status = db.Column(db.SmallInteger)

class Reservation(db.Model):
    id = db.Column('Id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.Id'), index = True)
    assigned_table_id = db.Column('tid', db.Integer, db.ForeignKey('table.Id')) # assigned table id
    num_of_customer = db.Column('num_cus', db.Integer)
    status = db.Column(db.SMALLINT, server_default=text('0'))
    res_datetime = db.Column('restime', db.DateTime, index=True)
    special_desc = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.now)


    RESERVATION_STATUS = (
        ('created', 1),
        ('cancelled', 2),
        ('unfinished', 3),
        ('done', 4)
    )


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('User', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('User', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class CartSchema(ma.ModelSchema):
    class Meta:
        model = Cart
        fields = ('id', 'user', 'menuItem_id')
cart_schema = CartSchema()
carts_schema = CartSchema(many=True)