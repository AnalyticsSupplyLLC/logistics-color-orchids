"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

#from flaskext import wtf
#from wtforms.form import Form
#from wtforms.fields import TextField,TextAreaField
from wtforms import fields
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.ext.appengine.ndb import model_form

from models import RouteEntryMain,RouteStops,DBEntry


class RouteEntry(FlaskForm):
    route_date = fields.DateField("route_date",validators=[DataRequired()])
    operator_name = fields.TextField("operator_name",validators=[DataRequired()])
    operator_pay = fields.FloatField('operator_pay', validators=[DataRequired()])
    hotel_expenses = fields.FloatField('hotel_expenses')
    fuel_expenses = fields.FloatField('fuel_expenses')
    fuel_gallons = fields.FloatField('fuel_gallons')
    total_miles = fields.FloatField('total_miles')
    total_hours = fields.FloatField('total_hours')

# App Engine ndb model form example
RouteForm = model_form(RouteEntryMain, FlaskForm, field_args={
    'route_date_start' : dict(validators=[DataRequired()],label="Start Date"),
    'route_date_end' : dict(validators=[DataRequired()],label="End Date"),
    'operator_name' : dict(validators=[DataRequired()]),
    'operator_pay' : dict(validators=[DataRequired()])
    #'example_name': dict(validators=[DataRequired()]),
    #'example_description': dict(validators=[DataRequired()]),
})

StopForm = model_form(RouteStops, FlaskForm, field_args={
    'stop_ship_to': dict(validators=[DataRequired()],label='Ship To'),
    'stop_load': dict(validators=[DataRequired()],label='Percent Load'),
    'stop_name':dict(label='Name'),'stop_zip':dict(label='Zip Code'),
    'stop_dist':dict(label='Distance'),'stop_pallets':dict(label='Num Pallets')
    ,'customer_cost':dict(label='Revenue'),
    'stop_ret_carts':dict(label='Num Return Carts'),'stop_carts':dict(label='Num Carts')})

def get_db_form():
    dbform = model_form(DBEntry, FlaskForm, field_args={
        'conn_name':dict(validators=[DataRequired()],label='Connection Name'),
        'conn_string':dict(validators=[DataRequired()],label='Connection String'),
        'conn_user':dict(validators=[DataRequired()],label='User Name'),
        'conn_pass':dict(validators=[DataRequired()],label='Password'),
        'conn_host':dict(validators=[DataRequired()],label='Database Host'),
        'conn_port':dict(validators=[DataRequired()],label='Database Port'),
        'conn_database':dict(validators=[DataRequired()],label='Database Name')})
    
    dbform.conn_pass = fields.PasswordField('Password', validators=[DataRequired()])
    return dbform()
