import re
from typing import Any
import flask
import flask_login
import flask_socketio
import flask_mdeditor
import flask_sqlalchemy
import os
import dotenv
import markdown2
from judges.judge import Judge
from constants import *

dotenv.load_dotenv()

default_keyword_arguments = {
  "user": flask_login.current_user
}

class TomChienXuOJMarkdown(markdown2.Markdown):
  @staticmethod
  def _convert_user_element(text: str) -> str:
    regex_user_element = "(\[user:(\w*)\])"
    for user_element in re.findall(regex_user_element, text):
      user = database_models.User.query.filter_by(username=user_element[1]).first()
      text = text.replace(user_element[0], f'<strike class="text-secondary">{user_element[1]}</strike> <b class="text-dark">(404: User Not Found)</b>' if not user else user.render_display)

    return text

  def convert(self, text):
    converted_text = super().convert(text)
    converted_text = self._convert_user_element(converted_text)

    return converted_text

markdown = TomChienXuOJMarkdown(extras=["break-on-newline", "code-friendly", "fenced-code-blocks", "footnotes", "spoiler", "strike"])

app = flask.Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_FILENAME}.db"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024 * MAX_FILE_CONTENT_SIZE
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

socketio = flask_socketio.SocketIO(app, async_mode="threading")
login_manager = flask_login.LoginManager(app)
mdeditor = flask_mdeditor.MDEditor(app)
database: flask_sqlalchemy.SQLAlchemy = flask_sqlalchemy.SQLAlchemy(app)

login_manager.login_view = "user.login"

global_OJ_judge = Judge("Paimon", "Con ma đang bay...", ["PYTHON3", "CPP20"])
global_OJ_judge.start()

class ErrorPage:
  def __init__(self, error_code: int, error: Exception, feedback: Any = None) -> None:
    self.error_code = error_code
    self.error = error
    self.feedback = feedback

  def set(self) -> Any:
    if self.error_code == 404:
      return flask.render_template("error/404.html", **default_keyword_arguments.copy(), error=self.error, feedback=self.feedback)

@app.errorhandler(404)
def _404(error):
  return ErrorPage(404, error).set()

from .socket_suppliers import *

from .user_pages import main_blueprint
app.register_blueprint(main_blueprint, url_prefix="/")

import database_models
with app.app_context():
  database.create_all()
  database_models.first_time_initialization()

@login_manager.user_loader
def load_user(user_id: int):
  return database_models.User.query.filter_by(id=user_id).first()