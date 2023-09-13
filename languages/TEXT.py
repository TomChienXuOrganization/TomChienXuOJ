from .base import CompilingExecutor

class Executor(CompilingExecutor):
  language_id = "TEXT"
  language_global_name = "Text Output Only"
  version = ""
  language_full_name = "Text Output Only"
  command = "type"
  command_args = []
  file_extension = "txt"
  compiled_file_extension = "txt"
  executable = "type"
  command_file_syntax = ["%original_file%"]
  header_code = ""
  example_code = """aaaaa"""