import flask
import flask_login
import flask_socketio
import flask_sqlalchemy
import flask_admin
import os
import dotenv
from settings import *

from .advanced_suppliers import TomChienXuOJ_render_template
from .advanced_suppliers import TomChienXuOJ_redirect
from .advanced_suppliers import default_keyword_arguments

dotenv.load_dotenv()

app = flask.Flask(__name__)

from .advanced_suppliers import TomChienXuAdminView
from .advanced_suppliers import TomChienXuAdminIndexView

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_FILENAME}.db"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024 * MAX_FILE_CONTENT_SIZE
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

socketio = flask_socketio.SocketIO(app)
login_manager = flask_login.LoginManager(app)
database = flask_sqlalchemy.SQLAlchemy(app)
admin = flask_admin.Admin(app, name="TomChienXuOJ", index_view=TomChienXuAdminIndexView())

login_manager.login_view = "user_view.login"

from tomchienxu_markdown.markdown import TomChienXuOJMarkdown
markdown = TomChienXuOJMarkdown()

from .socket_suppliers import *

global_OJ_judges = []
import database_models
from judges.judge import Judge
with app.app_context():
  database.create_all()
  database_models.first_time_initialization()
  database_models.every_time_initialization()

  judges = database_models.Judge.query.all()
  for judge in judges:
    new_judge = Judge(
      judge.name,
      judge.description,
      (USE_SOCKETIO_EVENT and judge.use_socketio_event_realtime),
      [language.language_id for language in judge.language],
      judge.authentication
    )
    global_OJ_judges.append(new_judge)

try:
  global_OJ_judge = global_OJ_judges[0]
except:
  global_OJ_judge = None

first_request = True
@app.before_request
def run_after_app_created():
  global first_request

  if flask.request.host not in ALLOWED_HOST:
    return "This is not a registered Base Domain!"

  if not first_request:
    return

  if global_OJ_judges:
    for judge in global_OJ_judges:
      judge.start()

  first_request = False

from .error_pages import ErrorPage
from . import user_pages
from . import utility_pages
app.register_blueprint(user_pages.main_blueprint, url_prefix="/")
app.register_blueprint(utility_pages.main_blueprint, url_prefix="/utility")

from . import admin_pages

login_manager.login_message = None
@login_manager.user_loader
def load_user(user_id: int):
  return database_models.User.query.filter_by(id=user_id).first()