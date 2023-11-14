from .base import CompilingExecutor
import sys

class Executor(CompilingExecutor):
  language_id = "PYTHON3"
  language_global_name = "Python"
  version = "3.11.3"
  language_full_name = "Python 3.11.3"
  command = "python"
  command_args = ["-m", "compileall", "-b"]
  file_extension = "py"
  compiled_file_extension = "pyc"
  executable = sys.executable
  command_file_syntax = ["%original_file%"]
  header_code = """
# import builtins
# TomChienXuOJ_WHITELISTED_LIBRARIES_%uuid% = ["math", "random", "sys", "time", "_io", "bisects", "datetime", "json"]
# TomChienXuOJ_ORIGINAL_IMPORT_%uuid% = builtins.__import__

# def TomChienXuOJ_SUB_IMPORT_%uuid%(name, *args, **kwargs):
#   if name in TomChienXuOJ_WHITELISTED_LIBRARIES_%uuid%:
#     return TomChienXuOJ_ORIGINAL_IMPORT_%uuid%(name, *args, **kwargs)
#   else:
#     raise ImportError(f"Module '{name}' is not allowed!")

# builtins.globals = None
# builtins.eval = None
# builtins.exec = None
# builtins.__import__ = TomChienXuOJ_SUB_IMPORT_%uuid%
"""
  example_code = """import sys, os
input()
a = 123
b = 456
c = 69420
d = 'abc'
"""