import flask_wtf
from wtforms import HiddenField, SelectField
from wtforms.validators import DataRequired

class ProblemSubmitForm(flask_wtf.FlaskForm):
  code = HiddenField(validators=[DataRequired()])
  language = SelectField("Programming Language", coerce=str, choices=[], validators=[DataRequired()])
