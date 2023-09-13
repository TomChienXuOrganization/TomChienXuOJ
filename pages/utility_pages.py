import flask
from . import default_keyword_arguments as d_kwargs
from forms import ProblemTemplateGenerator

main_blueprint = flask.Blueprint("utility_view", __name__)

@main_blueprint.route("/problem_template_generator")
def problem_template_generator():
  kwargs = d_kwargs.copy()

  form = ProblemTemplateGenerator()

  return flask.render_template(
    "utility/problem_template_generator.html",
    form=form,
    **kwargs
  )

@main_blueprint.route("/markdown")
def markdown_generator():
  kwargs = d_kwargs.copy()

  return flask.render_template(
    "utility/markdown.html",
    **kwargs
  )