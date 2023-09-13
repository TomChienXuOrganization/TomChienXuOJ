from pages import database

class TomChienXuOJ_SupportDefaultItems:
  @classmethod
  def initialize_default_items(cls) -> None:
    for item in [
      {header: value for header, value in zip(cls.default_item_headers, item)} for item in cls.default_items
    ]:
      for key, value in item.items():
        if type(value) in [list, dict, tuple]:
          item[key] = str(value)

      if not cls.query.filter_by(**item).first():
        new_item = cls(**item)
        database.session.add(new_item)
    database.session.commit()

from .InterfaceTheme import SiteTheme
from .InterfaceTheme import EditorTheme
from .Timezone import Timezone
from .Role import Permission
from .Role import Role
from .Role import Role_Permission
from .User import User
from .User import UserProfile
from .User import UserActivationStatus
from .Announcement import Announcement
from .Judge import Judge
from .Judge import ProgrammingLanguage
from .Judge import Judge_ProgrammingLanguage
from .Contest import Contest
from .Contest import Contest_Problem
from .ProblemAndSubmission import ProblemCategory
from .ProblemAndSubmission import ProblemJudgingType
from .ProblemAndSubmission import ProblemType
from .ProblemAndSubmission import Problem
from .ProblemAndSubmission import Submission
from .ProblemAndSubmission import Problem_BannedUser
from .ProblemAndSubmission import Problem_Publisher
from .ProblemAndSubmission import Problem_Tester
from .ProblemAndSubmission import Problem_ProblemType

def first_time_initialization() -> None:
  checker = False
  modals = [
    Permission,
    Role,
    ProblemCategory,
    ProblemJudgingType,
    ProgrammingLanguage,
    SiteTheme,
    EditorTheme,
    Timezone
  ]

  for modal in modals:
    if not modal.query.all():
      modal.initialize_default_items()
      checker = True

  if checker:
    print("""=======================================

>> When the first time initializing is finished, please (optional, but we recommend it) restart the application :D

=======================================""")

    with database.engine.connect() as connection:
      connection.execute(Role_Permission.insert().values(role_id=2, permission_id=1))
      connection.commit()

def every_time_initialization() -> None:
  # for permission in Permission.query.all().copy():
  #   setattr(Role, permission.name.upper(), property(lambda self: permission in self.permission))
  ...