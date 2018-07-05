from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
	post = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
	submit = SubmitField('Submit')