from json import loads
from pages import database
from os.path import exists
from . import TomChienXuOJ_SupportDefaultItems
from sqlalchemy.sql import func, expression
from helpers import TimezoneMixin
from settings import PROBLEM_TESTCASE_ROOT_STORAGE

Problem_ProblemType = database.Table(
  "re_problem_problem_type",
  database.Column("problem_id", database.Integer, database.ForeignKey("problem.id")),
  database.Column("problem_type_id", database.Integer, database.ForeignKey("problem_type.id"))
)

Problem_Publisher = database.Table(
  "re_problem_publisher",
  database.Column("problem_id", database.Integer, database.ForeignKey("problem.id")),
  database.Column("publisher_id", database.Integer, database.ForeignKey("user.id"))
)

Problem_Tester = database.Table(
  "re_problem_tester",
  database.Column("problem_id", database.Integer, database.ForeignKey("problem.id")),
  database.Column("publisher_id", database.Integer, database.ForeignKey("user.id"))
)

Problem_BannedUser = database.Table(
  "re_problem_banned_user",
  database.Column("problem_id", database.Integer, database.ForeignKey("problem.id")),
  database.Column("publisher_id", database.Integer, database.ForeignKey("user.id"))
)

class Problem(database.Model):
  id = database.Column(database.Integer, primary_key=True)
  problem_code = database.Column(database.String, nullable=False)
  author_id = database.Column(database.Integer, database.ForeignKey("user.id"), nullable=False)
  date_of_publishing = database.Column(database.DateTime(timezone=True), server_default=func.now())
  visibility = database.Column(database.Boolean, server_default=expression.true())
  problem_category_id = database.Column(database.Integer, database.ForeignKey("problem_category.id"), server_default="1")
  point = database.Column(database.Float, nullable=False)
  time_limit = database.Column(database.Float, server_default="1.0")
  memory_limit = database.Column(database.Integer, server_default="256")
  language_specific_resource_limits = database.Column(database.String, server_default="{}")
  problem_name = database.Column(database.String, nullable=False)
  problem_judging_type_id = database.Column(database.Integer, database.ForeignKey("problem_judging_type.id"), server_default="1")
  problem_legend = database.Column(database.Text, nullable=False)
  problem_editorial = database.Column(database.Text)
  problem_type = database.relationship("ProblemType", backref="problem_by_type", secondary=Problem_ProblemType)
  publisher = database.relationship("User", backref="published_problem", secondary=Problem_Publisher)
  tester = database.relationship("User", backref="tested_problem", secondary=Problem_Tester)
  banned_user = database.relationship("User", backref="problem_banned_on", secondary=Problem_BannedUser)
  submission = database.relationship("Submission", backref="problem")

  def __repr__(self):
    return f"{self.id}: {self.problem_code}"

  @property
  def is_submissible(self) -> bool:
    return exists(f"{PROBLEM_TESTCASE_ROOT_STORAGE}/{self.problem_code}/data.json")

class ProblemJudgingType(database.Model, TomChienXuOJ_SupportDefaultItems):
  id = database.Column(database.Integer, primary_key=True)
  name = database.Column(database.String, nullable=False)
  description = database.Column(database.Text)
  problem_in_this_judging_type = database.relationship("Problem", backref="problem_judging_type")

  def __repr__(self):
    return f"{self.id}: {self.name}"

  default_item_headers = ["name", "description"]
  default_items = [
    ["OI", ""],
    ["ICPC", ""],
  ]

class ProblemCategory(database.Model, TomChienXuOJ_SupportDefaultItems):
  id = database.Column(database.Integer, primary_key=True)
  name = database.Column(database.String, nullable=False)
  description = database.Column(database.Text)
  problem_in_this_category = database.relationship("Problem", backref="problem_category")

  def __repr__(self):
    return f"{self.id}: {self.name}"

  default_item_headers = ["name", "description"]
  default_items = [
    ["Uncategorized", ""]
  ]

class ProblemType(database.Model):
  id = database.Column(database.Integer, primary_key=True)
  name = database.Column(database.String)
  description = database.Column(database.Text)

  def __repr__(self):
    return f"{self.id}: {self.name}"

class Submission(database.Model, TimezoneMixin):
  id = database.Column(database.Integer, primary_key=True)
  code = database.Column(database.Text)
  judge_id = database.Column(database.Integer, database.ForeignKey("judge.id"))
  judge_authentication = database.Column(database.String)
  submission_authentication = database.Column(database.String)
  author_id = database.Column(database.Integer, database.ForeignKey("user.id"))
  problem_id = database.Column(database.Integer, database.ForeignKey("problem.id"))
  programming_language_id = database.Column(database.Integer, database.ForeignKey("programming_language.id"))
  time = database.Column(database.DateTime(timezone=True), server_default=func.now())
  result = database.Column(database.String, server_default="[]")
  judging = database.Column(database.Boolean)

  def __repr__(self):
    return f"{self.id}: {self.author.username}, on {self.problem.problem_name}"

  @property
  def status(self):
    judge_result = loads(self.result) if isinstance(self.result, str) else self.result
    for batch in judge_result:
      for case in batch:
        if case["status_code"] != "AC":
          return case["status_code"]
    else:
      return "AC"

  @property
  def correct_count(self):
    counter = 0
    judge_result = loads(self.result) if isinstance(self.result, str) else self.result
    for batch in judge_result:
      for case in batch:
        if case["accepted_or_not"]:
          counter += 1
    return counter

  @property
  def all_test_count(self):
    counter = 0
    judge_result = loads(self.result) if isinstance(self.result, str) else self.result
    for batch in judge_result:
      counter += len(batch)
    return counter

  @property
  def resources_used(self):
    time = 0
    memory = 0
    judge_result = loads(self.result) if isinstance(self.result, str) else self.result
    for batch in judge_result:
      for case in batch:
        time += case.get("time")
        memory += case.get("memory")
    return (round(time, 2), round(memory, 2))

  @property
  def time_timezone(self):
    return self.convert_time_as_timezone(self.time)