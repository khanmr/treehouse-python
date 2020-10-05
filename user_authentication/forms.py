from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField #, TextAreaField
from wtforms.validators import DataRequired, Email, Optional
#, Regexp, ValidationError, Length, EqualTo

class RegisterForm(Form):
    """Tacocat Registration Form
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password2', validators=[DataRequired()])
    
class LoginForm(Form):
    """Tacocat Login Form
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class TacoForm(Form):
    """Tacocat Taco Form
    """
    protein = StringField('Protein', validators=[DataRequired()])
    shell = StringField('Shell', validators=[DataRequired()])
    cheese = BooleanField('Cheese?', validators=[Optional()],
                          default=False)
    extras = StringField('Extras?', validators=[Optional()])
    
