from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
	SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired,\
	Email, EqualTo, Length
from flask import request


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class MessageForm(FlaskForm):
    message = TextAreaField(('Message'), validators=[
        DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])

# class SearchForm(FlaskForm):
#     q = StringField('Search', validators=[DataRequired()])

#     def __init__(self, *args, **kwargs):
#     	if 'formdata' not in kwargs:
#     		kwargs['formdata'] = request.args
#     	if 'csrf_enabled' not in kwargs:
#     		kwargs['csrf_enabled'] = False
#     	super(SearchForm, self).__init__(*args, **kwargs)