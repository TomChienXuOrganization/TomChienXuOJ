from pages import database
from flask_login import UserMixin

class User(UserMixin, database.Model):
  id = database.Column(database.Integer, primary_key=True, unique=True, nullable=False)
  username = database.Column(database.String, unique=True, nullable=False)
  email = database.Column(database.String, unique=True, nullable=False)
  password = database.Column(database.String, nullable=False)
  role_id = database.Column(database.Integer, database.ForeignKey("role.id"), nullable=False)

  announcements = database.relationship("Announcement", backref="user")

  @property
  def username_display(self) -> str:
    return self.role.display.replace("$username$", self.username)

  @property
  def render_display(self) -> str:
    return f'<a href="#" class="text-decoration-none" style="color: {self.role.color};"><b>{self.username_display}</b></a>'