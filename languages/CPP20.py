from .base import CompilingExecutor

class Executor(CompilingExecutor):
  id = "CPP20"
  language_global_name = "C++"
  version = "20"
  language_full_name = "C++ 20"
  command = "g++"
  command_args = []
  file_extension = "cpp"
  compiled_file_extension = "out"
  executable = ""
  command_file_syntax = ["%original_file%", "-o", "%output_file%"]
  example_code = """#include <bits/stdc++.h>
using namespace std;

int main() {
  cout << "Con ma nang cao";
}
"""