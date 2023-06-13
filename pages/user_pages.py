from __future__ import annotations
from datetime import datetime
import flask
import flask_login
import importlib
from sqlalchemy import desc
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from json import loads
from json import dumps
from . import default_keyword_arguments as d_kwargs
from . import markdown
from . import ErrorPage
from . import global_OJ_judge
from . import database
from database_models import User
from database_models import Announcement
from forms import LoginForm
from forms import SignupForm
from forms import ProblemSubmitForm
from constants import LANGUAGE_EXECUTOR_ROOT_STORAGE

main_blueprint = flask.Blueprint("user", __name__)

db_con = None
Problem = None

@main_blueprint.route("/a", methods=["GET", "POST"])
@flask_login.login_required
def a():
  if flask.request.method == "POST":
    title = flask.request.form.get("title")
    announcement = flask.request.form.get("announcement")
    author = flask_login.current_user.id

    new_announcement = Announcement(author=author, title=title, announcement=announcement)
    database.session.add(new_announcement)
    database.session.flush()
    database.session.commit()

  return flask.render_template(
    "admin/announcement/create.html",
    **d_kwargs.copy()
  )

@main_blueprint.route("signup", methods=["GET", "POST"])
def signup():
  kwargs = d_kwargs.copy()
  def returner(reason: str = None, input_form = None) -> str:
    return flask.render_template(
      "signup.html",
      failed_signup_authorization_reason=reason,
      form=input_form,
      **kwargs
    )

  if flask_login.current_user.is_authenticated:
    return flask.redirect(flask.url_for("user.home"))

  form = SignupForm()

  if form.validate_on_submit():
    username = form.username.data
    email = form.email.data
    password = form.password.data
    confirm_password = form.confirm_password.data
    user = User.query.filter_by(email=email).first()

    if user:
      return returner("Email already existed.", form)

    if len(email) < 4:
      return returner("Email must be greater than 3 characters.", form)

    if len(username) < 2:
      return returner("Username must be greater than 1 character.", form)

    if password != confirm_password:
      return returner("Passwords don't match.", form)

    if len(password) < 7:
      return returner("Password must be at least 7 characters.", form)

    new_user = User(username=username, email=email, password=generate_password_hash(password, method="sha256"), role_id=1)
    database.session.add(new_user)
    database.session.flush()
    database.session.commit()
    return flask.redirect(flask.url_for("user.login", **kwargs))

  return flask.render_template("signup.html", form=form, **kwargs)

@main_blueprint.route("login", methods=["GET", "POST"])
def login():
  kwargs = d_kwargs.copy()
  def returner(reason: str = None, input_form = None) -> str:
    return flask.render_template(
      "login.html",
      failed_login_authorization_reason=reason,
      form=input_form,
      **kwargs
    )

  if flask_login.current_user.is_authenticated:
    return flask.redirect(flask.url_for("user.home"))

  form = LoginForm()

  if form.validate_on_submit():
    email = form.email.data
    password = form.password.data
    user = User.query.filter_by(email=email).first()

    if not user:
      return returner("No user to be found.", form)

    if not check_password_hash(user.password, password):
      return returner("Password not match.", form)

    flask_login.login_user(user)
    return flask.redirect(flask.url_for("user.home"))

  return flask.render_template("login.html", form=form, **kwargs)

@main_blueprint.route("/logout")
def logout():
  flask_login.logout_user()
  return flask.redirect(flask.url_for("user.login"))

@main_blueprint.route("/")
def home():
  kwargs = d_kwargs.copy()
  announcement_data = [a.__dict__ for a in Announcement.query.order_by(desc(Announcement.id)).all()]
  for announcement in announcement_data:
    announcement["author"] = User.query.filter_by(id=announcement["author"]).first()
    announcement["announcement"] = markdown.convert(announcement["announcement"])

  return flask.render_template(
    "user/home/home.html",
    announcements=announcement_data,
    **kwargs
  )

@main_blueprint.route("/about")
def about():
  kwargs = d_kwargs.copy()

  return flask.render_template(
    "user/home/about_and_judges.html",
    **kwargs
  )

from judges.judge import Judge
@main_blueprint.route("/judges")
def judges():
  kwargs = d_kwargs.copy()

  return flask.render_template(
    "user/home/judges.html",
    status={
      Judge("Kay/O", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Chamber", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Killjoy", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Sage", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Omen", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Viper", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Fade", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Sova", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Yoru", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Raze", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Jett", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Brimstone", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Gekko", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Phoenix", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Reyna", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Breach", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Skye", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Astra", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Neon", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Harbor", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      Judge("Cypher", "Con nhện đang bay...", ["PYTHON3", "CPP20"]): global_OJ_judge.language_statuses.copy(),
      global_OJ_judge: global_OJ_judge.language_statuses.copy()
    },
    **kwargs
  )

@main_blueprint.route("/problems/<string:problem_code>", methods=["GET", "POST"])
def problem_view(problem_code):
  kwargs = d_kwargs.copy()

  with db_con:
    problem = db_con.cursor().execute("SELECT * FROM Problem WHERE problem_code = ?", (problem_code, )).fetchone()

  if not problem:
    return ErrorPage(404, Exception(f"No problems named {problem_code}")).set()

  problem["author"] = User.from_id(problem["author"])
  problem["problem_data"] = loads(problem["problem_data"])

  for md_key in ["editorial"]:
    problem[md_key] = markdown.convert(problem[md_key])

  for user_key in ["publishers", "testers", "banned_users"]:
    if isinstance(problem["problem_data"][user_key], list):
      problem["problem_data"][user_key] = [User.from_id(id) for id in loads(problem["problem_data"][user_key])]

  for md_key in ["problem_legend", "problem_input", "problem_output", "problem_clarification", "problem_source"]:
    if problem["problem_data"][md_key] is not None:
      problem["problem_data"][md_key] = markdown.convert(problem["problem_data"][md_key])

  for example in problem["problem_data"]["problem_examples"]:
    for md_key in ["input", "output", "explanation"]:
      if example[md_key] is not None:
        example[md_key] = markdown.convert(example[md_key])

  return flask.render_template(
    "user/problem/problem.html",
    **kwargs,
    problem=problem
  )

@main_blueprint.route("/problems/<string:problem_code>/submit", methods=["GET", "POST"])
def problem_submit(problem_code):
  kwargs = d_kwargs.copy()

  with db_con:
    problem = db_con.cursor().execute("SELECT * FROM Problem WHERE problem_code = ?", (problem_code, )).fetchone()

  if not problem:
    flask.abort(404, Exception(f"No problems named {problem_code}."))

  problem["author"] = User.from_id(problem["author"])
  problem["problem_data"] = loads(problem["problem_data"])

  for user_key in ["publishers", "testers", "banned_users"]:
    if isinstance(problem["problem_data"][user_key], list):
      problem["problem_data"][user_key] = [User.from_id(id) for id in loads(problem["problem_data"][user_key])]

  form = ProblemSubmitForm()
  form.language.choices = [(
    language,
    importlib.import_module(f"{LANGUAGE_EXECUTOR_ROOT_STORAGE}.{language}").Executor.language_full_name
  ) for language in [language for language, status in global_OJ_judge.language_statuses.items() if status["status"]]]

  if form.validate_on_submit():
    judge_process = global_OJ_judge.initialize_judging_process(
      "dinhcao_viethoangpopping",
      "OI",
      form.language.data,
      form.code.data,
    )
    
    data = {
      "code": form.code.data,
      "problem": Problem.from_id(1),
      "author": User.from_id(1),
      "language": importlib.import_module(f"{LANGUAGE_EXECUTOR_ROOT_STORAGE}.{form.language.data}").Executor,
      "submitted_at": datetime.now(),
      "result": global_OJ_judge.execute_all_judging_process(judge_process)
    }

    return flask.render_template(
      "user/submission/submission.html",
      data=data,
      **d_kwargs.copy()
    )
    return 
    # return flask.redirect(flask.url_for("user.problem_submit", problem_code="cses1635"))

  return flask.render_template(
    "user/problem/submit.html",
    **kwargs,
    problem=problem,
    form=form
  )

@main_blueprint.route("/submissions/<int:submission_id>")
def submission_view(submission_id):
  data = {
    "code": "print(sum(map(int, input().split())))",
    "problem": Problem.from_id(1),
    "author": User.from_id(1),
    "language": importlib.import_module(f"{LANGUAGE_EXECUTOR_ROOT_STORAGE}.PYTHON3").Executor,
    "submitted_at": "05/26/2023, 23:18:37",
    "result": []
  }

  return flask.render_template(
    "user/submission/submission.html",
    data=data,
    **d_kwargs.copy()
  )