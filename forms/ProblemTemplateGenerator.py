import flask_wtf
from wtforms import SubmitField, TextAreaField

class ProblemTemplateGenerator(flask_wtf.FlaskForm):
  legend = TextAreaField("Problem Introduction/Legend")
  input_specification = TextAreaField("Input Specification")
  output_specification = TextAreaField("Output Specification")
  submit = SubmitField("Generate")