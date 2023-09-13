import flask
from typing import Any
from . import app
from . import default_keyword_arguments

class ErrorPage:
  def __init__(self, error_code: int, error: Exception, feedback: Any = None) -> None:
    self.error_code = error_code
    self.error = error
    self.feedback = feedback

  def set(self) -> Any:
    if self.error_code == 404:
      return flask.render_template("error/404.html", **default_keyword_arguments.copy(), error=self.error, feedback=self.feedback)

    if self.error_code == 405:
      return flask.render_template("error/404.html", **default_keyword_arguments.copy(), error=self.error, feedback=self.feedback)

    if self.error_code == 403:
      return flask.render_template("error/403.html", **default_keyword_arguments.copy(), error=self.error, feedback=self.feedback)

@app.errorhandler(405)
def _405(error):
  return ErrorPage(405, error).set()

@app.errorhandler(404)
def _404(error):
  return ErrorPage(404, error).set()

@app.errorhandler(403)
def _403(error):
  return ErrorPage(403, error).set()