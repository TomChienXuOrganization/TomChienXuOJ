import os
import threading
import traceback
import sys
import waitress
from typing import Any
from constants import *
from pages import app

def TomChienXuOJ_crash_exception_traceback_handler(__exception_type, __base_exception, __traceback_type) -> Any:
  """For security reasons, the TomChienXuOJ's developers have hidden the absolute paths pointing to the files where the exceptions occur."""

  exception = traceback.TracebackException(__exception_type, __base_exception, __traceback_type)
  for frame_summary in exception.stack:
    frame_summary.filename = os.path.relpath(frame_summary.filename)

  print("".join(exception.format()), file=sys.stderr)

sys.excepthook = TomChienXuOJ_crash_exception_traceback_handler
sys.dont_write_bytecode = True

def run_application(debug: bool = False) -> None:
  app.run(host="0.0.0.0", port=443, debug=debug, ssl_context=("server.pem", "server-key.pem"))

def run_server() -> None:
  server = threading.Thread(target=run_application)
  server.start()
  waitress.serve(app, host="0.0.0.0", port=443, url_scheme="https")

if __name__ == "__main__":
  run_application(True)
  # run_server()
