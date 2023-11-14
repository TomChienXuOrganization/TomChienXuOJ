from helpers import TimezoneMixin
from pages import database
from sqlalchemy.sql import func, expression

class Announcement(database.Model, TimezoneMixin):
  id = database.Column(database.Integer, primary_key=True, unique=True)
  author_id = database.Column(database.Integer, database.ForeignKey("user.id"))
  title = database.Column(database.String, nullable=False)
  time = database.Column(database.DateTime(timezone=True), server_default=func.now())
  announcement = database.Column(database.Text, nullable=False)
  visibility = database.Column(database.Boolean, server_default=expression.true())

  def __repr__(self):
    return f"{self.id}: {self.title}"

  @property
  def time_timezone(self):
    return self.convert_time_as_timezone(self.time)

  default_item_headers = ["title", "announcement"]
  default_items = [
    ["Some default flat pages", "- [Custom Checker](/flat/custom_checker)\n- [Status Codes](/flat/status_codes)"]
  ]