import flask_wtf
from wtforms import SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired

class LoginForm(flask_wtf.FlaskForm):
  email = EmailField("Email Address", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField("Login")