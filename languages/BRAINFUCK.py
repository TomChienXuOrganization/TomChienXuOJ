from .base import CompilingExecutor

class Executor(CompilingExecutor):
  language_id = "BRAINFUCK"
  language_global_name = "Brainfuck"
  version = ""
  language_full_name = "Brainfuck"
  command = "bf"
  command_args = []
  file_extension = "bf"
  compiled_file_extension = "bfc"
  executable = ""
  command_file_syntax = []
  example_code = """++++"""