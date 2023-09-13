from .base import CompilingExecutor

class Executor(CompilingExecutor):
  language_id = "PASCAL"
  language_global_name = "Pascal"
  version = "1.0.12"
  language_full_name = "Pascal 1.0.12"
  command = "fpc"
  command_args = []
  file_extension = "pas"
  compiled_file_extension = "exe"
  executable = ""
  command_file_syntax = ["%original_file%"]
  header_code = ""
  example_code = """"""