from . import TomChienXuOJ_SupportDefaultItems
from pages import database
from sqlalchemy.sql import expression

class SiteTheme(database.Model, TomChienXuOJ_SupportDefaultItems):
  id = database.Column(database.Integer, primary_key=True, unique=True)
  theme = database.Column(database.String, unique=True)

  user_profile_using_this_theme = database.relationship("UserProfile", backref="site_theme")

  def __repr__(self):
    return f"{self.id}: {self.theme}"

  default_item_headers = ["theme"]
  default_items = [
    ["light"],
    ["dark"],
    ["dracula"]
  ]

class EditorTheme(database.Model, TomChienXuOJ_SupportDefaultItems):
  id = database.Column(database.Integer, primary_key=True, unique=True)
  name =  database.Column(database.String, unique=True)
  theme = database.Column(database.String, unique=True)
  dark_theme = database.Column(database.Boolean)

  user_profile_using_this_theme = database.relationship("UserProfile", backref="editor_theme")

  def __repr__(self):
    return f"{self.id}: {self.theme}"

  default_item_headers = ["name", "theme", "dark_theme"]
  default_items = [
    ["Chrome", "chrome", expression.false()],
    ["Clouds", "clouds", expression.false()],
    ["Crimson Editor", "crimson_editor", expression.false()],
    ["Dawn", "dawn", expression.false()],
    ["Dreamweaver", "dreamweaver", expression.false()],
    ["Eclipse", "eclipse", expression.false()],
    ["GitHub", "github", expression.false()],
    ["IPlastic", "iplastic", expression.false()],
    ["Solarized Light", "solarized_light", expression.false()],
    ["TextMate", "textmate", expression.false()],
    ["Tomorrow", "tomorrow", expression.false()],
    ["XCode", "xcode", expression.false()],
    ["Kuroir", "kuroir", expression.false()],
    ["KatzenMilch", "katzenmilch", expression.false()],
    ["SQL Server", "sqlserver", expression.false()],
    ["Ambiance", "ambiance", expression.true()],
    ["Chaos", "chaos", expression.true()],
    ["Clouds Midnight", "clouds_midnight", expression.true()],
    ["Dracula", "dracula", expression.true()],
    ["Cobalt", "cobalt", expression.true()],
    ["Gruvbox", "gruvbox", expression.true()],
    ["Green on Black", "gob", expression.true()],
    ["idle Fingers", "idle_fingers", expression.true()],
    ["krTheme", "kr_theme", expression.true()],
    ["Merbivore", "merbivore", expression.true()],
    ["Merbivore Soft", "merbivore_soft", expression.true()],
    ["Mono Industrial", "mono_industrial", expression.true()],
    ["Monokai", "monokai", expression.true()],
    ["Nord Dark", "nord_dark", expression.true()],
    ["One Dark", "one_dark", expression.true()],
    ["Pastel on dark", "pastel_on_dark", expression.true()],
    ["Solarized Dark", "solarized_dark", expression.true()],
    ["Terminal", "terminal", expression.true()],
    ["Tomorrow Night", "tomorrow_night", expression.true()],
    ["Tomorrow Night Blue", "tomorrow_night_blue", expression.true()],
    ["Tomorrow Night Bright", "tomorrow_night_bright", expression.true()],
    ["Tomorrow Night 80s", "tomorrow_night_eighties", expression.true()],
    ["Twilight", "twilight", expression.true()],
    ["Vibrant Ink", "vibrant_ink", expression.true()],
    ["GitHub Dark", "github_dark", expression.true()]
  ]