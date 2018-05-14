from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import StringField, PasswordField, BooleanField, SubmitField

from ..models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(4, 16)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(4, 16)])
    password = PasswordField('Password', validators=[DataRequired(), 
                                                     EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])   
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username {} already in use.'.format(field.data))
