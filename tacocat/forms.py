from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import (DataRequired, Regexp, ValidationError, 
                               Length, EqualTo, Optional)

from models import User


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('Username already exists.')


class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word with letters, "
                         "numbers, and underscores only.")
            ),
            name_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )
    

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class TacoForm(Form):
    protein = StringField('Protein', validators=[DataRequired()])
    shell = StringField('Shell', validators=[DataRequired()])
    cheese = BooleanField('Cheese?', validators=[Optional()],
                          default=False)
    extras = StringField('Extras?', validators=[Optional()])