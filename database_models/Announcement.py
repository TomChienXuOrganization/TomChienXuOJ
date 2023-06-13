from pages import database
from sqlalchemy.sql import func, expression

class Announcement(database.Model):
  id = database.Column(database.Integer, primary_key=True, unique=True, nullable=False)
  title = database.Column(database.String, nullable=False)
  time = database.Column(database.DateTime(timezone=True), server_default=func.now())
  announcement = database.Column(database.Text, nullable=False)
  visibility = database.Column(database.Boolean, nullable=False, server_default=expression.true())
  author = database.Column(database.Integer, database.ForeignKey("user.id"), nullable=False)
