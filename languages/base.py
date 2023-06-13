from typing import Any, List, Union

class CompilingExecutor:
  id: str
  language_global_name: str
  version: Any
  language_full_name: str
  command: str
  command_args: List[Union[str, Any]]
  file_extension: str
  compiled_file_extension: str
  executable: Any
  example_code: str
  command_file_syntax: str

  @classmethod
  @property
  def compile_command(cls) -> str:
    return f"{cls.command} {' '.join(cls.command_args)} {' '.join(cls.command_file_syntax)}"

  @classmethod
  def get_compile_command(cls):
    return cls.compile_command