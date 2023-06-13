import flask_wtf
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, FloatField, IntegerField, TextAreaField
from wtforms.validators import DataRequired

class CreateProblemForm(flask_wtf.FlaskForm):
  problem_code = StringField
  visibility = BooleanField
  # date_of_publishing
  # author
  problem_category = SelectField
  problem_types = SelectField
  points = FloatField
  time_limit = FloatField
  memory_limit = FloatField
  editorial = TextAreaField
  publishers = SelectField
  testers = SelectField
  problem_name = StringField
  problem_judging_type = StringField
  banned_users = SelectField
  problem_legend = TextAreaField
  problem_input = TextAreaField
  problem_output = TextAreaField
  problem_examples = TextAreaField
  problem_clarification = TextAreaField
  problem_source = TextAreaField