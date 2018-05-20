from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length
from wtforms import StringField, TextAreaField, SubmitField

from ..models import User, Post


class CreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    tags = StringField('Tags')
    body = TextAreaField('Body')
    submit = SubmitField('Save')

class UpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    tags = StringField('Tags')
    body = TextAreaField('Body')
    submit = SubmitField('Save')

class ProfileEditForm(FlaskForm):
    body = TextAreaField('Body')
    submit = SubmitField('Submit')
