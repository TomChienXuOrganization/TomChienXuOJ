from . import TomChienXuOJ_SupportDefaultItems
from pages import database

Role_Permission = database.Table(
  "re_role_permission",
  database.Column("role_id", database.Integer, database.ForeignKey("role.id")),
  database.Column("permission_id", database.Integer, database.ForeignKey("permission.id"))
)

class Role(database.Model, TomChienXuOJ_SupportDefaultItems):
  id = database.Column(database.Integer, primary_key=True, unique=True)
  name = database.Column(database.String, unique=True, nullable=False)
  display = database.Column(database.String)
  color = database.Column(database.String)

  permission = database.relationship("Permission", backref="role_has_this_permission", secondary=Role_Permission)
  user_who_has_this_role = database.relationship("User", backref="role")

  def __repr__(self):
    return f"{self.id}: {self.name}"

  def check(self, permission_name: str) -> bool:
    return permission_name in [permission.name for permission in self.permission]

  default_item_headers = ["name", "display", "color"]
  default_items = [
    ["User", "$username$", "#1b1b1b"],
    ["Admin", "🔥 $username$", "#d0312d"]
  ]

class Permission(database.Model, TomChienXuOJ_SupportDefaultItems):
  id = database.Column(database.Integer, primary_key=True, unique=True)
  name = database.Column(database.String, unique=True, nullable=False)
  description = database.Column(database.Text)

  def __repr__(self):
    return f"{self.id}: {self.name}"

  default_item_headers = ["name", "description"]
  default_items = [
    ["ADMIN", "Admin access granted: Be able to do everything on site."],
    ["VIEW_PRIVATE_ANNOUNCEMENTS", "Be able to view all announcements which have been created (even private ones)."],
    ["VIEW_PRIVATE_PROBLEMS", "Be able to view all problems which have been created (even private ones)."]
  ]