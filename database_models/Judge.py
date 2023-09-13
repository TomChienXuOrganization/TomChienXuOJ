from . import TomChienXuOJ_SupportDefaultItems
from pages import database
from sqlalchemy.sql import expression
import sys

Judge_ProgrammingLanguage = database.Table(
  "re_judge_programming_language",
  database.Column("judge_id", database.Integer, database.ForeignKey("judge.id")),
  database.Column("programming_language_id", database.Integer, database.ForeignKey("programming_language.id"))
)

class Judge(database.Model):
  id = database.Column(database.Integer, primary_key=True)
  name = database.Column(database.String, unique=True, nullable=False)
  authentication = database.Column(database.String, unique=True)
  description = database.Column(database.String)
  use_socketio_event_realtime = database.Column(database.Boolean, server_default=expression.true())
  language = database.relationship("ProgrammingLanguage", backref="judge_has_this_programming_language", secondary=Judge_ProgrammingLanguage)
  submission = database.relationship("Submission", backref="judge")

  def __repr__(self):
    return f"{self.id}: {self.name}"

class ProgrammingLanguage(database.Model, TomChienXuOJ_SupportDefaultItems):
  id = database.Column(database.Integer, primary_key=True)
  language_id = database.Column(database.String, unique=True, nullable=False)
  language_global_name = database.Column(database.String, unique=True, nullable=False)
  version = database.Column(database.String)
  language_full_name = database.Column(database.String, nullable=False)
  command = database.Column(database.String)
  command_args = database.Column(database.String, server_default="[]")
  file_extension = database.Column(database.String)
  compiled_file_extension = database.Column(database.String)
  executable = database.Column(database.String)
  command_file_syntax = database.Column(database.String, server_default="[]")
  example_code = database.Column(database.String)
  submission = database.relationship("Submission", backref="programming_language")
  user_by_default_programming_language = database.relationship("UserProfile", backref="programming_language")

  def __repr__(self):
    return f"{self.id}: {self.language_full_name}"

  default_item_headers = ["language_id", "language_global_name", "version", "language_full_name", "command", "command_args", "file_extension", "compiled_file_extension", "executable", "command_file_syntax", "example_code"]
  default_items = [
    ["PYTHON3", "Python", "3.11.3", "Python 3.11.3", "python", ["-m", "compileall", "-b"], "py", "pyc", sys.executable, ["%original_file%"], "input()"],
    ["CPP20", "C++", "20", "C++ 20", "g++", [], "cpp", "out", "", ["%original_file%", "-o", "%output_file%"], ""],
    ["TEXT", "Text Output Only", "", "Text Output Only", "type", [], "txt", "txt", "type", ["%original_file%"], "aaaaaaa"]
  ]