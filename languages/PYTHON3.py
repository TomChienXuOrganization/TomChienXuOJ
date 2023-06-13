from .base import CompilingExecutor
import sys

class Executor(CompilingExecutor):
  id = "PYTHON3"
  language_global_name = "Python"
  version = "3.11.3"
  language_full_name = "Python 3.11.3"
  command = "python"
  command_args = ["-m", "compileall", "-b"]
  file_extension = "py"
  compiled_file_extension = "pyc"
  executable = sys.executable
  command_file_syntax = ["%original_file%"]
  example_code = """import sys, os
input()
a = 123
b = 456
c = 69420
d = 'abc'
"""