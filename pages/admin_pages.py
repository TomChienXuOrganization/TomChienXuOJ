from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt
from markupsafe import Markup
from . import TomChienXuAdminView

def bool_formatter(view, value, name):
  label = f'{name}: {"true" if value else "false"}'
  true_icon = f'<i class="bi bi-check-square-fill" style="color: green" title="{label}"></i>'
  false_icon = f'<i class="bi bi-x-square-fill" style="color: red" title="{label}"></i>'
  return Markup(true_icon if value else false_icon)

TOMCHIENXU_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
TOMCHIENXU_FORMATTERS.update({bool: bool_formatter})

class TomChienXuModelView(TomChienXuAdminView, ModelView):
  column_type_formatters = TOMCHIENXU_FORMATTERS
  can_view_details = True
  can_export = True
  named_filter_urls = True
  can_set_page_size = True

  def get_column_type(self, column_name):
    if self.model is None:
      return None
    model_class = self.model
    column_property = getattr(model_class, column_name, None)

    if column_property is not None:
      column_type = column_property.expression.type
      return column_type
    else:
      return None

  def render(self, *args, **kwargs):
    kwargs["get_column_type"] = self.get_column_type
    return super().render(*args, **kwargs)


from . import database
from . import admin
import database_models

class AdminView_User(TomChienXuModelView):
  column_exclude_list = ["password"]

class AdminView_UserActivationStatus(TomChienXuModelView):
  pass

class AdminView_Role(TomChienXuModelView):
  pass

class AdminView_Permission(TomChienXuModelView):
  pass

class AdminView_Announcement(TomChienXuModelView):
  column_exclude_list = ["announcement"]
  column_default_sort = ("time", True)

class AdminView_Judge(TomChienXuModelView):
  pass

class AdminView_ProgrammingLanguage(TomChienXuModelView):
  column_exclude_list = ["command", "command_args", "executable", "command_file_syntax", "example_code"]

class AdminView_ProblemCategory(TomChienXuModelView):
  pass

class AdminView_ProblemJudgingType(TomChienXuModelView):
  pass

class AdminView_ProblemType(TomChienXuModelView):
  pass

class AdminView_Problem(TomChienXuModelView):
  column_exclude_list = ["language_specific_resource_limits", "problem_legend", "problem_input", "problem_output", "problem_example", "problem_clarification", "problem_editorial", "problem_source"]
  column_default_sort = ("date_of_publishing", True)

class AdminView_Contest(TomChienXuModelView):
  ...

class AdminView_Submission(TomChienXuModelView):
  column_exclude_list = ["code", "result", "judge_authentication"]
  column_default_sort = ("time", True)
  can_create = False

admin.add_view(AdminView_User(database_models.User, database.session))
admin.add_view(AdminView_User(database_models.UserActivationStatus, database.session))
admin.add_view(AdminView_Role(database_models.Role, database.session))
admin.add_view(AdminView_Permission(database_models.Permission, database.session))
admin.add_view(AdminView_Announcement(database_models.Announcement, database.session))
admin.add_view(AdminView_Judge(database_models.Judge, database.session))
admin.add_view(AdminView_ProgrammingLanguage(database_models.ProgrammingLanguage, database.session))
admin.add_view(AdminView_ProblemCategory(database_models.ProblemCategory, database.session))
admin.add_view(AdminView_ProblemJudgingType(database_models.ProblemJudgingType, database.session))
admin.add_view(AdminView_ProblemType(database_models.ProblemType, database.session))
admin.add_view(AdminView_Problem(database_models.Problem, database.session))
admin.add_view(AdminView_Contest(database_models.Contest, database.session))
admin.add_view(AdminView_Submission(database_models.Submission, database.session))