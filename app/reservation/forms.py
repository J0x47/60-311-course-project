from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField, TextAreaField, DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from ..models import Reservation


class ReservationForm(FlaskForm):
    """
    Form for customers to create reservations
    """
    num_of_customers = StringField('Number of People', validators=[DataRequired()])
    reservation_dateTime = DateTimeField(id='res_datetime', format=('%d/%m/%Y %H:%M:%S'))
    special_desc = TextAreaField('Sepcial description')
    submit = SubmitField('Submit')