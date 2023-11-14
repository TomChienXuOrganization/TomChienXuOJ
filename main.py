import sys
from helpers import TomChienXuOJ_crash_exception_traceback_handler, create_sub_path_if_not_exists, get_files
from settings import (
  DOMAIN,
  PORT,
  DEBUG_STATUS,
  SSL_CONTEXT,
  USE_SSL_CONTEXT_ON_MAIN_SERVER,
  PROBLEM_TESTCASE_ROOT_STORAGE
)
from pages import app

sys.excepthook = TomChienXuOJ_crash_exception_traceback_handler
sys.dont_write_bytecode = False

default_folders = [PROBLEM_TESTCASE_ROOT_STORAGE]

def run_application() -> None:
  app.run(host=DOMAIN, port=PORT, debug=DEBUG_STATUS, ssl_context=SSL_CONTEXT if USE_SSL_CONTEXT_ON_MAIN_SERVER else None)

if __name__ == "__main__":
  for folder in default_folders:
    create_sub_path_if_not_exists(folder)
  if not ".env" in get_files("."):
    with open(".env", "w", encoding="utf-8") as file:
      file.write("SECRET_KEY=")

  run_application()
