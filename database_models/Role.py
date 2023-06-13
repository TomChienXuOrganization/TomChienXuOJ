from pages import database
from json import dumps

class Role(database.Model):
  id = database.Column(database.Integer, primary_key=True, unique=True, nullable=False)
  name = database.Column(database.String, unique=True, nullable=False)
  display = database.Column(database.String, nullable=False)
  color = database.Column(database.String, nullable=False)
  permissions = database.Column(database.String, nullable=False, server_default="{}")

  users_who_have_this_role = database.relationship("User", backref="role")

  @staticmethod
  def initialize_default_roles() -> None:
    initialize_roles = {
      "User": {
        "name": "User",
        "display": "$username$",
        "color": "#1b1b1b",
        "permissions": dumps({"admin_permission_bypass": False}, ensure_ascii=True, sort_keys=True)
      },
      "Admin": {
        "name": "Admin",
        "display": "🔥 $username$",
        "color": "#d0312d",
        "permissions": dumps({"admin_permission_bypass": True}, ensure_ascii=True, sort_keys=True)
      }
    }
    for _, role in initialize_roles.items():
      if not Role.query.filter_by(name=role.get("name")).first():
        new_role = Role(**role)
        database.session.add(new_role)
        database.session.commit()

def first_time_initialization() -> None:
  role_data = Role.query.all()
  if not role_data:
    Role.initialize_default_roles()
    print("""=======================================

>> When the first time initializing is finished, please (optional, but we recommend it) restart the application :D

=======================================""")