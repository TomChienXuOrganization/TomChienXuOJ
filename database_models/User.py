from pages import database
from flask_login import UserMixin
from sqlalchemy.sql import expression

class User(UserMixin, database.Model):
  id = database.Column(database.Integer, primary_key=True, unique=True)
  username = database.Column(database.String, unique=True, nullable=False)
  email = database.Column(database.String, unique=True, nullable=False)
  password = database.Column(database.String, nullable=False)
  role_id = database.Column(database.Integer, database.ForeignKey("role.id"))
  activation = database.Column(database.Boolean, server_default=expression.false())
  two_fa_authentication = database.Column(database.Boolean, server_default=expression.false())

  profile = database.relationship("UserProfile", backref="user", uselist=False)
  announcement = database.relationship("Announcement", backref="author")
  problem = database.relationship("Problem", backref="author")
  submission = database.relationship("Submission", backref="author")
  activation_status = database.relationship("UserActivationStatus", backref="user")
  contest = database.relationship("Contest", backref="author")

  def __repr__(self):
    return f"{self.id}: {self.username}"

  @property
  def username_display(self) -> str:
    return self.role.display.replace("$username$", self.username)

  @property
  def render_display(self) -> str:
    return f'<a href="#" style="color: {self.role.color};"><b>{self.username_display}</b></a>'

class UserActivationStatus(database.Model):
  id = database.Column(database.Integer, primary_key=True, unique=True)
  user_id = database.Column(database.Integer, database.ForeignKey("user.id"))
  uuid = database.Column(database.String, nullable=False)
  verification_code = database.Column(database.String, nullable=False)

  def __repr__(self):
    return f"{self.id}: {self.user.username}"

class UserProfile(database.Model):
  id = database.Column(database.Integer, primary_key=True, unique=True)
  user_id = database.Column(database.Integer, database.ForeignKey("user.id"))
  full_name = database.Column(database.Text)
  description = database.Column(database.Text)
  time_zone_id = database.Column(database.Integer, database.ForeignKey("timezone.id"))
  default_programming_language_id = database.Column(database.Integer, database.ForeignKey("programming_language.id"))
  site_theme_id = database.Column(database.Integer, database.ForeignKey("site_theme.id"))
  editor_theme_id = database.Column(database.Integer, database.ForeignKey("editor_theme.id"))
  attending_contest_id = database.Column(database.Integer, database.ForeignKey("contest.id"))

  def __repr__(self):
    return f"{self.id}: (Profile) {self.user.username}"