from settings import DATABASE_FILENAME
from werkzeug.security import check_password_hash
from sys import exit
import sqlite3
import getpass

print("""TomChienXuOJ Account System - v1.0-beta;
Heyyyy! Thanks for using our service of Online Judge System - TomChienXuOJ.
Instead of letting you create an administrator account like others, here, you have to create an account for yourself first!
Since we want to make sure that you MUST HAVE ACCESSED the site, we will not create a super-user, you have to do it by your own.
""")

email = input("Account Email: ")
username = input("Account Username: ")
password = getpass.getpass("Account Password (Hidden and Secured): ")

connection = sqlite3.connect(f"instance/{DATABASE_FILENAME}.db")

result = connection.execute("SELECT * FROM user WHERE username = ? AND email = ?", (username, email)).fetchone()

if not result:
  print("\nNo users have been found :<")
  exit(0)

if not check_password_hash(result[3], password):
  print("\nPassword not match :<")
  exit(0)

connection.execute("UPDATE user SET role_id = 2 WHERE id = ?", (result[0],))
connection.commit()
print("\nSet to Administrator successfully!")