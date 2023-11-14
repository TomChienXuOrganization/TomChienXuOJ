from flask import redirect
from flask import url_for
from flask import abort
from flask import request
from flask import render_template
from flask_login import current_user
from flask_admin import expose
from flask_admin import BaseView
from flask_admin import AdminIndexView
from settings import SHOW_STANDARD_ERROR
from helpers import TimezoneMixin

default_keyword_arguments = {
  "user": current_user,
  "SHOW_STANDARD_ERROR": SHOW_STANDARD_ERROR,
  "TimezoneMixin": TimezoneMixin
}

def TomChienXuOJ_render_template(*args, **kwargs):
  return render_template(*args, **default_keyword_arguments, **kwargs)

def TomChienXuOJ_redirect(location, code=302, *args, **kwargs):
    return redirect(request.args.get("next") or location, code, *args, **kwargs)

class TomChienXuAdminView(BaseView):
  custom_error_page_handler = {
    0: "GRANTED",
    1: "UNDEFINED",
    2: "NO_USER_LOGGED_IN",
    3: "NO_PERMISSION_GRANTED"
  }

  def __init__(self, *args, **kwargs):
    self.custom_error_code = 0
    super().__init__(*args, **kwargs)

  def is_accessible(self):
    if not current_user.is_authenticated:
      self.custom_error_code = 2
      return False

    if not current_user.role.check("ADMIN"):
      self.custom_error_code = 3
      return False

    return True

  def inaccessible_callback(self, name, **kwargs):
    if self.custom_error_code == 2:
      return redirect(url_for("user_view.login"))
    elif self.custom_error_code == 3:
      abort(403)
    else:
      abort(404)

  def render(self, *args, **kwargs):
    kwargs.update(default_keyword_arguments)
    return super().render(*args, **kwargs)

class TomChienXuAdminIndexView(TomChienXuAdminView, AdminIndexView):
  @expose()
  def index(self):
    # psutil.cpu_percent(1)
    # psutil.virtual_memory()[2]
    # psutil.virtual_memory()[3]/1000000000
    return self.render(self._template)