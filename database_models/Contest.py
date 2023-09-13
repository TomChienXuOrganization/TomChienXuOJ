from helpers import TimezoneMixin
from pages import database
from sqlalchemy.sql import expression, func

Contest_Problem = database.Table(
  "re_contest_problem",
  database.Column("contest_id", database.Integer, database.ForeignKey("contest.id")),
  database.Column("problem_id", database.Integer, database.ForeignKey("problem.id")),
  database.Column("point", database.Float),
  database.Column("visibility", database.Boolean, server_default=expression.true())
)

class Contest(database.Model, TimezoneMixin):
  id = database.Column(database.Integer, primary_key=True)
  contest_code = database.Column(database.String, unique=True, nullable=False)
  contest_name = database.Column(database.String, nullable=False)
  author_id = database.Column(database.Integer, database.ForeignKey("user.id"))
  visibility = database.Column(database.Boolean, server_default=expression.true())
  scoreboard_visibility = database.Column(database.Boolean, server_default=expression.true())
  allow_comments = database.Column(database.Boolean, server_default=expression.true())
  allow_problem_tags = database.Column(database.Boolean, server_default=expression.true())
  run_pretests_only = database.Column(database.Boolean, server_default=expression.true())
  number_of_precision_digit = database.Column(database.Integer, server_default="2")
  start_time = database.Column(database.DateTime(timezone=True), server_default=func.now())
  end_time = database.Column(database.DateTime(timezone=True), server_default=func.now())
  time_limitation = database.Column(database.Integer, server_default=str(10 * 60 * 60)) # a.k.a Duration, default: 10 hours
  problem_set = database.relationship("Problem", backref="included_in_contest", secondary=Contest_Problem)
  description = database.Column(database.Text)
  access_code = database.Column(database.String)
  moss = database.Column(database.Boolean, server_default=expression.false())

  contestant = database.relationship("UserProfile", backref="contest")

  def __repr__(self):
    return f"{self.id}: {self.contest_name}"

  @property
  def start_time_timezone(self):
    return self.convert_time_as_timezone(self.start_time)

  @property
  def end_time_timezone(self):
    return self.convert_time_as_timezone(self.end_time)