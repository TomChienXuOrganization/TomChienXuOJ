import os
import traceback
import sys
from typing import Any
from settings import *
from pages import app

def TomChienXuOJ_crash_exception_traceback_handler(__exception_type, __base_exception, __traceback_type) -> Any:
  """For security reasons, the TomChienXuOJ's developers have hidden the absolute paths pointing to the files where the exceptions occur."""

  exception = traceback.TracebackException(__exception_type, __base_exception, __traceback_type)
  for frame_summary in exception.stack:
    frame_summary.filename = os.path.relpath(frame_summary.filename)

  print("".join(exception.format()), file=sys.stderr)

sys.excepthook = TomChienXuOJ_crash_exception_traceback_handler
sys.dont_write_bytecode = False

def run_application() -> None:
  app.run(host=DOMAIN, port=PORT, debug=DEBUG_STATUS, ssl_context=SSL_CONTEXT if USE_SSL_CONTEXT_ON_MAIN_SERVER else None)

if __name__ == "__main__":
  run_application()
