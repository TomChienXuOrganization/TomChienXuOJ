from __future__ import annotations
import re
import zipfile
import smtplib
import ssl
import dotenv
import os
import flask_login
from flask import abort
from flask import url_for
from flask import jsonify
from flask import Blueprint
from flask_login import current_user
from flask_login import login_required
from email.message import EmailMessage
from email.mime.text import MIMEText
from sqlalchemy import desc
from sqlalchemy.sql import expression
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from json import loads
from json import dumps
from threading import Thread
from . import markdown
from . import global_OJ_judge
from . import global_OJ_judges
from . import database
from . import TomChienXuOJ_render_template as render_template
from . import TomChienXuOJ_redirect as redirect
from . import app
from database_models import User
from database_models import UserProfile
from database_models import UserActivationStatus
from database_models import Announcement
from database_models import Problem
from database_models import Contest
from database_models import Contest_Problem
from database_models import Judge
from database_models import ProgrammingLanguage
from database_models import Submission
from forms import LoginForm
from forms import SignupForm
from forms import ProblemSubmitForm
from forms import UploadCaseForm
from forms import UploadCustomChecker
from uuid import uuid4
from settings import MAX_NUMBER_OF_SUBMISSIONS_PER_USER
from settings import PROBLEM_TESTCASE_ROOT_STORAGE
from settings import ACTIVATION_EMAIL_SENDER
from settings import FULL_DOMAIN_WITH_SCHEME
from settings import SMTP_PORT
from settings import SMTP_SENDING_SERVER
from settings import SEND_ACTIVATION_EMAIL
from helpers import *

dotenv.load_dotenv()

main_blueprint = Blueprint("user_view", __name__)

# @app.route("/restart", methods=["GET", "POST"])
# def restart_server():
#   os.kill(os.getpid(), signal.SIGINT)
#   return "Server is restarting..."

@main_blueprint.route("signup", methods=["GET", "POST"])
def signup():
  def returner(reason: str = None, input_form = None) -> str:
    return render_template(
      "authentication/signup.html",
      failed_signup_authorization_reason=reason,
      form=input_form
    )

  if current_user.is_authenticated:
    return redirect(url_for("user_view.home"))

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

    new_user = User(
      username=username,
      email=email,
      password=generate_password_hash(password, method="scrypt"),
      role_id=1,
      activation=(not SEND_ACTIVATION_EMAIL)
    )
    database.session.add(new_user)
    database.session.commit()

    new_user_profile = UserProfile(user_id = new_user.id)
    database.session.add(new_user_profile)
    database.session.commit()

    if not SEND_ACTIVATION_EMAIL:
      return redirect(url_for("user_view.login"))
    else:
      verification_uuid, verification_code = str(uuid4()), str(uuid4())

      new_status = UserActivationStatus(user_id=new_user.id, uuid=verification_uuid, verification_code=verification_code)
      database.session.add(new_status)
      database.session.commit()

      def send_email():
        with app.app_context():
          with smtplib.SMTP_SSL(SMTP_SENDING_SERVER, SMTP_PORT, context=ssl.create_default_context()) as server:
            server.login(ACTIVATION_EMAIL_SENDER, os.getenv("EMAIL_PASSWORD"))
            message = EmailMessage()
            message["From"] = ACTIVATION_EMAIL_SENDER
            message["To"] = email
            message["Subject"] = "TomChienXu Online Judge - Activation Email"
            message.attach(MIMEText(render_template("authentication/activation_email.html", activation_link=f"{FULL_DOMAIN_WITH_SCHEME}/activation/{verification_uuid}/{verification_code}"), "html"))
            server.send_message(message)

      Thread(target=send_email).start()
      return render_template("authentication/activation_email_sent.html")

  return render_template("authentication/signup.html", form=form)

@main_blueprint.route("login", methods=["GET", "POST"])
def login():
  def returner(reason: str = None, input_form = None) -> str:
    return render_template(
      "authentication/login.html",
      failed_login_authorization_reason=reason,
      form=input_form
    )

  if current_user.is_authenticated:
    return redirect(url_for("user_view.home"))

  form = LoginForm()

  if form.validate_on_submit():
    email = form.email.data
    password = form.password.data
    user = User.query.filter_by(email=email).first()

    if not user:
      return returner("No user to be found.", form)

    if not check_password_hash(user.password, password):
      return returner("Password not match.", form)

    if not user.activation:
      return returner("This user has not been activated.", form)

    flask_login.login_user(user)
    return redirect(url_for("user_view.home"))

  return render_template("authentication/login.html", form=form)

@main_blueprint.route("/logout")
def logout():
  flask_login.logout_user()
  return redirect(url_for("user_view.login"))

@main_blueprint.route("/")
def home():
  with database.session.no_autoflush:
    if current_user.is_authenticated and current_user.role.check("VIEW_PRIVATE_ANNOUNCEMENTS"): 
      announcements = Announcement.query.order_by(desc(Announcement.id)).all()
    else:
      announcements = Announcement.query.filter_by(visibility=True).order_by(desc(Announcement.id)).all()
    for announcement in announcements:
      announcement.announcement = markdown.convert(announcement.announcement)

    return render_template(
      "user/home/home.html",
      announcements=announcements
    )

@main_blueprint.route("/activation/<string:uuid>/<string:verification_code>")
def activate_account(uuid: str, verification_code: str):
  status = UserActivationStatus.query.filter_by(uuid=uuid, verification_code=verification_code).first()

  if not status:
    return render_template("authentication/activated_unsuccessfully.html")

  User.query.filter_by(id=status.user_id).first().activation = expression.true()
  database.session.delete(status)
  database.session.commit()

  return render_template("authentication/activated_successfully.html")

@main_blueprint.route("/about")
def about():
  return render_template("user/home/about.html")

@main_blueprint.route("/judges")
def judges():
  status = {
    judge: judge.language_statuses.copy() for judge in global_OJ_judges
  } if global_OJ_judges else {}

  languages = {}
  for judge_status in list(status.values()):
    for language_id, language_status in list(judge_status.items()):
      languages.update({language_id: language_status.get("display_name", "Not Found")})

  return render_template(
    "user/home/judges.html",
    status=status,
    languages=languages
  )

@main_blueprint.route("/problems", defaults={"page": 1})
@main_blueprint.route("/problems/<int:page>")
def problem_list(page = 1):
  if current_user.is_authenticated and current_user.profile.attending_contest_id:
    problems = Problem.query.filter(Problem.problem_name.in_([problem.problem_name for problem in current_user.profile.contest.problem_set])).paginate(page=page)
  else:
    if current_user.is_authenticated and current_user.role.check("VIEW_PRIVATE_PROBLEMS"):
      pagination = database.select(Problem)
    else:
      pagination = database.select(Problem).where(Problem.visibility == 1)
    problems = database.paginate(pagination, page=page, per_page=100)

  return render_template("user/problem/list.html", problems=problems, endpoint="user_view.problem_list")

@main_blueprint.route("/p/<string:problem_code>", methods=["GET", "POST"])
def problem_view(problem_code):
  with database.session.no_autoflush:
    problem = Problem.query.filter_by(problem_code=problem_code).first()

    if not problem:
      abort(404, f"No problems named {problem_code}.")

    for markdown_key in ["problem_legend", "problem_editorial"]:
      if getattr(problem, markdown_key) is not None:
        setattr(problem, markdown_key, markdown.convert(getattr(problem, markdown_key)) if getattr(problem, markdown_key) else False)

    for json_key in ["language_specific_resource_limits",]:
      try:
        value = loads(getattr(problem, json_key))
      except:
        value = {}
      setattr(problem, json_key, value)

    return render_template(
      "user/problem/problem.html",
      problem=problem
    )

@main_blueprint.route("/p/<string:problem_code>/testcase", methods=["GET", "POST"])
def problem_testcase_management(problem_code):
  def returner(reason: str = None, upload_form = None, problem = None) -> str:
    return render_template(
      "user/problem/testcase_management.html",
      failed_upload_reason=reason,
      upload_form=upload_form,
      problem=problem
    )

  upload_form = UploadCaseForm()
  upload_custom_checker_form = UploadCustomChecker()

  with database.session.no_autoflush:
    problem = Problem.query.filter_by(problem_code=problem_code).first()

    parent_folder_directory = os.path.join(PROBLEM_TESTCASE_ROOT_STORAGE, problem_code)
    if upload_form.validate_on_submit():
      zip_file = upload_form.zip_compressed_case_file.data
      filename = secure_filename(zip_file.filename)

      if not check_extension(filename):
        return returner("The case file was unsuccessfully uploaded due to not having the right extension. Please retry with another file whose extension is <b>.zip</b>!", upload_form = upload_form, problem = problem)

      create_sub_path_if_not_exists(parent_folder_directory)
      file_full_directory = os.path.join(parent_folder_directory, filename)
      zip_file.save(file_full_directory)

      with zipfile.ZipFile(file_full_directory, "r") as zip:
        zip.extractall(parent_folder_directory)

      files = get_files(f"{PROBLEM_TESTCASE_ROOT_STORAGE}/{problem_code}")

      input_files = sorted(re.findall(r"(\d+)\.in", " ".join(files)), key=lambda x: int(x))
      output_files = sorted(re.findall(r"(\d+)\.out", " ".join(files)), key=lambda x: int(x))

      problem_cases_new_data = {
        "allow_submitting": True,
        "custom_checker": None,
        "cases": [[]]
      }

      for input_file in input_files:
        case_data = {"input_file": f"{input_file}.in"}
        if input_file in output_files:
          case_data["output_file"] = f"{input_file}.out"
        case_data["point"] = 1.0
        problem_cases_new_data["cases"][0].append(case_data)

      save_json_data(f"{PROBLEM_TESTCASE_ROOT_STORAGE}/{problem_code}/data.json", problem_cases_new_data)

      os.remove(file_full_directory)

    if upload_custom_checker_form.validate_on_submit():
      custom_checker = upload_custom_checker_form.custom_checker.data
      create_sub_path_if_not_exists(parent_folder_directory)
      if os.path.exists(os.path.join(parent_folder_directory, "data.json")):
        problem_cases_new_data = get_json_data(f"{PROBLEM_TESTCASE_ROOT_STORAGE}/{problem_code}/data.json")
        print(custom_checker)
        problem_cases_new_data["custom_checker"] = custom_checker
        save_json_data(f"{PROBLEM_TESTCASE_ROOT_STORAGE}/{problem_code}/data.json", problem_cases_new_data)

    if not problem:
      abort(404, f"No problems named {problem_code}.")

    if os.path.exists(parent_folder_directory):
      files = get_files(f"{PROBLEM_TESTCASE_ROOT_STORAGE}/{problem_code}")
    else:
      files = []

    if os.path.exists(os.path.join(parent_folder_directory, "data.json")):
      problem_cases_data = get_json_data(f"{PROBLEM_TESTCASE_ROOT_STORAGE}/{problem_code}/data.json")
      custom_checker = problem_cases_data.get("custom_checker")
    else:
      problem_cases_data = custom_checker = None

    sub_kwargs = {
      "upload_form": upload_form,
      "upload_custom_checker_form": upload_custom_checker_form,
      "problem": problem,
      "files": files,
      "custom_checker": custom_checker or "",
      "problem_cases_data": problem_cases_data
    }

    return render_template("user/problem/testcase_management.html", **sub_kwargs)

@main_blueprint.route("/p/<string:problem_code>/submit", methods=["GET", "POST"])
@login_required
def problem_submit(problem_code):
  form = ProblemSubmitForm()
  form.language.choices = [(
    language,
    ProgrammingLanguage.query.filter_by(language_id=language).first().language_full_name
  ) for language in [language for language, status in global_OJ_judge.language_statuses.items() if status["status"]]] if global_OJ_judge else []

  if form.validate_on_submit():
    if problem_code not in get_sub_directories(PROBLEM_TESTCASE_ROOT_STORAGE):
      abort(404, f"No cases for this problem named {problem_code} have been found.")

    problem_data = get_json_data(f"{PROBLEM_TESTCASE_ROOT_STORAGE}/{problem_code}/data.json")

    if not problem_data.get("allow_submitting"):
      abort(403, f"The author of this problem {problem_code} (or an administrator) has disabled submitting status for this one. You are not allowed to submit to this problem! Try again later.")

    if Submission.query.filter_by(judging=1, author_id=current_user.id).count() >= MAX_NUMBER_OF_SUBMISSIONS_PER_USER:
      abort(404, f"You can't submit more than {MAX_NUMBER_OF_SUBMISSIONS_PER_USER} submissions at a time!")

    judge_process_authentication = global_OJ_judge.initialize_judging_process(
      problem_code,
      "OI",
      form.language.data,
      form.code.data
    )
    
    new_submission = Submission(
      code = form.code.data,
      judge_id = Judge.query.filter_by(name=global_OJ_judge.name).first().id,
      judge_authentication = global_OJ_judge.authentication,
      submission_authentication = judge_process_authentication,
      author_id = current_user.id,
      problem_id = Problem.query.filter_by(problem_code=problem_code).first().id,
      programming_language_id = ProgrammingLanguage.query.filter_by(language_id=form.language.data).first().id,
      judging = 1
    )
    database.session.add(new_submission)
    database.session.commit()

    def finish_judging_process(id):
      with app.app_context():
        result = global_OJ_judge.execute_all_judging_process(judge_process_authentication)
        submission = Submission.query.filter_by(id=id).first()
        submission.result = dumps(result, ensure_ascii=True)
        submission.judging = 0
        database.session.commit()

    if global_OJ_judge.socket_supported and form.language.data != "TEXT":
      Thread(target=finish_judging_process, args=[new_submission.id]).start()
    else:
      finish_judging_process(new_submission.id)

    return redirect(url_for("user_view.submission_view", submission_id=new_submission.id))

  with database.session.no_autoflush:
    problem = Problem.query.filter_by(problem_code=problem_code).first()

    if not problem:
      abort(404, f"No problems named {problem_code}.")

    return render_template(
      "user/problem/submit.html",
      problem=problem,
      form=form,
      no_judges_running=not (global_OJ_judge)
    )

@main_blueprint.route("/submissions", defaults={"page": 1})
@main_blueprint.route("/submissions/<int:page>")
def submission_list(page = 1):
  submissions = database.paginate(database.select(Submission).order_by(desc(Submission.time)), page=page)
  return render_template("user/submission/list.html", submissions=submissions, endpoint="user_view.submission_list")

@main_blueprint.route("/submissions/mine", defaults={"page": 1})
@main_blueprint.route("/submissions/mine/<int:page>")
@login_required
def my_submission_list(page = 1):
  submissions = database.paginate(database.select(Submission).where(Submission.author == current_user).order_by(desc(Submission.time)), page=page)
  return render_template("user/submission/list.html", submissions=submissions, endpoint="user_view.my_submission_list")

@main_blueprint.route("/s/<int:submission_id>/rejudge", methods=["POST"])
def submission_rejudge(submission_id):
  if not current_user.is_authenticated or not current_user.role.check("ADMIN"):
    return jsonify({"status": "error", "error_log": "You don't have permissions to access and execute this action!"}), 403

  submission = Submission.query.filter_by(id=submission_id).first()
  if not submission:
    return jsonify({"status": "error", "error_log": f"No submission whose ID is {submission_id}."}), 404

  judge_process_authentication = global_OJ_judge.initialize_judging_process(
    submission.problem.problem_code,
    "OI",
    submission.programming_language.language_id,
    submission.code
  )

  submission.submission_authentication = judge_process_authentication
  submission.result = dumps([])
  submission.judging = 1
  database.session.commit()
  
  def finish_judging_process(id):
    with app.app_context():
      submission = Submission.query.filter_by(id=id).first()
      result = global_OJ_judge.execute_all_judging_process(judge_process_authentication)
      submission.result = dumps(result, ensure_ascii=True)
      submission.judging = 0
      database.session.commit()

  Thread(target=finish_judging_process, args=[submission_id]).start()
  return jsonify({"status": "success"}), 200

@main_blueprint.route("/s/<int:submission_id>")
@login_required
def submission_view(submission_id):
  with database.session.no_autoflush:
    submission = Submission.query.filter_by(id=submission_id).first()

    if not submission:
      abort(404, f"No submission whose ID is {submission_id}.")

    submission.result = loads(submission.result)
    submission.markdown_code = markdown.convert(
f"""```{submission.programming_language.file_extension}
{submission.code}
```"""
    )

    return render_template(
      "user/submission/submission.html",
      submission=submission
    )

@main_blueprint.route("/users", defaults={"page": 1})
@main_blueprint.route("/users/<int:page>")
def user_list(page = 1):
  users = database.paginate(database.select(User), page=page)
  return render_template("user/user/list.html", users=users)

@main_blueprint.route("/u/<string:username>")
def user_profile_view(username):
  return render_template(f"user/user/profile.html")

@main_blueprint.route("/tournaments")
def tournament_list():
  return redirect(url_for("user_view.tournament_view", year=2023))

@main_blueprint.route("/t/<int:year>")
def tournament_view(year = 2023):
  return render_template(f"user/tournament/{year}.html")

@main_blueprint.route("/contests", defaults={"page": 1})
@main_blueprint.route("/contests/<int:page>")
def contest_list(page = 1):
  contests = database.paginate(database.select(Contest).order_by(desc(Contest.start_time)), page=page)
  return render_template("user/contest/list.html", contests=contests)

@main_blueprint.route("/c/<string:contest_code>")
@login_required
def contest_view(contest_code): 
  with database.session.no_autoflush as session:
    contest = Contest.query.filter_by(contest_code=contest_code).first()

    if not contest:
      abort(404, f"No contest whose code is {contest_code}.")

    contest_problem_set_data = {
      problem: session.query(Contest_Problem).filter_by(contest_id=contest.id, problem_id=problem.id).first() for problem in contest.problem_set
    }

    contest.description = markdown.convert(contest.description)

    return render_template(
      "user/contest/contest.html",
      contest=contest,
      contest_problem_set_data=contest_problem_set_data
    )