import flask_wtf
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired

class SignupForm(flask_wtf.FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  email = EmailField("Email Address", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
  submit = SubmitField("Sign up")