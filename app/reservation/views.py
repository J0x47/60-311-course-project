from flask import url_for, abort, render_template, redirect, flash, request, session
from flask_login import login_required, current_user
from app.models import Reservation, User
from . import reservation_blueprint as reservation
from forms import ReservationForm
from app import db
from sqlalchemy import and_, or_, not_
from flask_wtf import Form
from wtforms.fields import DateField, DateTimeField

@reservation.route('/reservations')
@login_required
def view_reservations():
    """
    list all reservation order by created time (desc)
    """
    user_id = current_user.id
    userobj = User.query.filter_by(id=user_id).first()

    all_reservations = Reservation.query.filter_by(user_id=current_user.id).order_by(Reservation.created_on.desc()).all()

    return render_template('reservation/reservations.html', userobj=userobj,
                           reservation_list=all_reservations, title="Reservation List")


@reservation.route('/reservation/confirm')
@login_required
def confirm_reservation():
    """
    confirmation of reservation information for customers
    """
    user_id = current_user.id
    # reservation_id = session['rid']
    r_obj = Reservation.query.filter(Reservation.user_id == user_id).order_by(Reservation.created_on.desc()).first()
    # query = db.session().query(Reservation, User)
    # query = query.join(User, Reservation.user_id == User.id)\
    #     .filter(and_(Reservation.user_id == user_id, Reservation.status == 0)).all()
    # userobj = query[0].User
    userobj = User.query.filter_by(id=user_id).first()

    return render_template('reservation/reservation_confirm.html',
                           reservation_obj=r_obj, userobj=userobj, title="Reservation")


@reservation.route('/reservation', methods=['GET', 'POST'])
@login_required
def make_reservation():
    """
    make a reservation
    """
    user_id = current_user.id
    form = ReservationForm()
    rid=None
    if form.validate_on_submit():
        res_datetime=None
        reservation_obj = Reservation(user_id=user_id,
                                      num_of_customer=form.num_of_customers.data,
                                      res_datetime=form.reservation_dateTime.data.strftime('%Y-%m-%d %H:%M'),
                                      special_desc=form.special_desc.data)

        try:
            # add reservation_obj to the database, default status = 0; 1 for created (confirmed by user)
            db.session.add(reservation_obj)
            db.session.commit()
            # r = Reservation.query.filter(and_(Reservation.user == user_id,
            #                                   Reservation.res_datetime == res_datetime)).first()
            # rid=r.id
            flash('You have submitted a reservation request.')
        except:
            #
            flash('Error: unknown!')
        session['rid']=rid
        # redirect to reservation confirmation page
        return redirect(url_for('reservation.confirm_reservation'))

    # load reservation template
    return render_template('reservation/reservation.html',
                           form=form,
                           title="Make a Reservation")



# datetimepicker
class MyForm(Form):
    date = DateField(id='datepick')

@reservation.route('/res')
def index():
    form = MyForm()
    return render_template('reservation/res.html', form=form)


class DateForm(Form):
    dt = DateField('Pick a Date', format="%m/%d/%Y")

@reservation.route('/dform', methods=['post','get'])
def home():
    form = DateForm()
    if form.validate_on_submit():
        return form.dt.data.strftime('%x')
    return render_template('reservation/vort.html', form=form)


        # pub_time = request.form.get('publish_time')
        # update_time = request.form.get('update_time')
        #
        # if pub_time:
        #     post.pub_time = datetime.datetime.strptime(pub_time, "%Y-%m-%d %H:%M:%S")
        #
        # if update_time:
        #     post.update_time = datetime.datetime.strptime(update_time, "%Y-%m-%d %H:%M:%S")




class DateTimeForm(Form):
    DateTime = DateTimeField(id='res_datetime')

@reservation.route('/dtform', methods=['post','get'])
def dthome():
    form = DateTimeForm()
    # if form.validate_on_submit():
    #     return form.dt.data.strftime('%Y-%m-%d %H:%M:%S')
    return render_template('reservation/res_test.html', form=form)