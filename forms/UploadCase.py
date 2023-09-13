from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, HiddenField

class UploadCaseForm(FlaskForm):
  zip_compressed_case_file = FileField(validators=[FileRequired()])
  submit = SubmitField("Upload Cases")

class UploadCustomChecker(FlaskForm):
  custom_checker = HiddenField()
  submit = SubmitField("Upload Custom Checker")