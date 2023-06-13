import flask_wtf
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(flask_wtf.FlaskForm):
  email = StringField("Email Address", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField("Login")