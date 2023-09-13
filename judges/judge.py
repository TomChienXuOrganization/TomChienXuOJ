from __future__ import annotations

from helpers import get_json_data
from languages.base import CompilingExecutor
from .judge_result import JudgeResult
from typing import *
import sys
import os
import importlib
import traceback
import subprocess
import uuid
import tempfile
import logging
import threading
import traceback
import shutil
import psutil
import time
import datetime
import socketio

from settings import JUDGE_SERVER_ROOT_STORAGE
from settings import PROBLEM_TESTCASE_ROOT_STORAGE
from settings import BYPASSED_DEFAULT_CMD_COMMANDS
from settings import LANGUAGE_EXECUTOR_ROOT_STORAGE
from settings import FULL_DOMAIN_WITH_SCHEME
from settings import USE_SOCKETIO_EVENT
from settings import SAFE_FIRST_START_AFTER_COMPILING
from settings import SSL_VERIFY

class TomChienXuOJThread(threading.Thread):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self._return = None

  def run(self) -> None:
    if self._target is not None:
      self._return = self._target(*self._args, **self._kwargs)

  def join(self, *args, **kwargs) -> Any:
    threading.Thread.join(self, *args, **kwargs)
    return self._return

def TomChienXuOJ_crash_exception_traceback_handler(__exception_type, __base_exception, __traceback_type) -> None:
  """For security reasons, the TomChienXuOJ's developers have hidden the absolute paths pointing to the files where the exceptions occur."""

  exception = traceback.TracebackException(__exception_type, __base_exception, __traceback_type)
  for frame_summary in exception.stack:
    frame_summary.filename = os.path.relpath(frame_summary.filename)

  print("".join(exception.format()), file=sys.stderr)

sys.excepthook = TomChienXuOJ_crash_exception_traceback_handler

logger = logging.getLogger("TomChienXuJudge")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s | %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)

def standard_checker(process_output: str, judge_input: str, judge_output: str, accepted_point: Union[float, int], time: float, memory: int) -> JudgeResult:
  """
    Checking every single character must be similar to the answer.
  """

  if process_output == judge_output:
    return JudgeResult(True, process_output, "AC", time, memory, "", accepted_point, "(*≧︶≦))(￣▽￣* )ゞ Ayy you got it!")
  else:
    return JudgeResult(False, process_output, "WA", time, memory, "", 0, "(≧﹏≦) Life doesn't always operate like the way we want! Be strong!")

class JudgeProcess:
  def __init__(self, judger: Judge, problem_code: str, judge_type: str, programming_language: str, code: str, checker: Callable) -> None:
    self.language_package: CompilingExecutor = importlib.import_module(f"{LANGUAGE_EXECUTOR_ROOT_STORAGE}.{programming_language}").Executor
    self.judger: Judge = judger
    self.problem_code: str = problem_code
    self.judge_type: str = judge_type
    self.programming_language: str = programming_language
    self.authentication: str = str(uuid.uuid4())
    self.code: str = self.language_package.header_code.replace("%uuid%", self.authentication.replace("-", "")) + code
    self.checker: Callable = checker
    self.judge_folder: tempfile.TemporaryDirectory = tempfile.TemporaryDirectory(prefix="TomChienXuOJQualified_", suffix=f"_Judge_{self.judger.authentication.replace('-', '')}_{self.authentication.replace('-', '')}")
    self.original_file: str = f"{self.problem_code}.{self.language_package.file_extension}"
    self.output_file: str = f"{self.problem_code}.{self.language_package.compiled_file_extension}"
    self.full_directory: str = os.path.join(self.judge_folder.name, self.original_file)
    self.full_output_directory = os.path.join(self.judge_folder.name, self.output_file)
    self.compilable: bool = True
    self.compile_error: Any = None
    self.compile_status: Any = self.write_and_compile()

    if not self.compile_status[0]:
      self.compilable = False
      self.compile_error = self.compile_status[1]

  def write_and_compile(self) -> Tuple[Union[bool, JudgeResult]]:
    start = time.perf_counter()
    with open(self.full_directory, "w", encoding="utf-8") as file:
      file.write(self.code)

    command = self.language_package.get_compile_command().replace("%original_file%", self.full_directory).replace("%output_file%", self.full_output_directory)
    with subprocess.Popen(
      command,
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      universal_newlines=True,
      shell=True
    ) as compiling_process:
      output, error = [item.replace("\r\n", "\n").strip("\n") for item in compiling_process.communicate()]

      logger.info(f"Compile time: {time.perf_counter() - start}s")
      if compiling_process.returncode != 0:
        return False, JudgeResult(False, "An exception has occurred!", "RTE", 9999, 9999, error or output, 0, "The compiler is working fine, but your code isn't. (┬┬﹏┬┬)")
      else:
        return (True,)

  def process(self, judge_input: str, judge_output: str, accepted_point: Union[float, int] = 0.1, timeout: Union[float, int] = 1.0) -> JudgeResult:
    if not self.compilable:
      return self.compile_error

    if judge_input:
      judge_input: str = judge_input.replace("\r\n", "\n").strip("\n")
    if judge_output:
      judge_output: str = judge_output.replace("\r\n", "\n").strip("\n")

    command = [self.language_package.executable, self.full_output_directory] if self.language_package.executable else self.full_output_directory
    with subprocess.Popen(
      command,
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      universal_newlines=True,
      cwd=self.judge_folder.name,
      shell=True
    ) as process:
      try:
        def judge():
          # process.stdin.write(judge_input)
          # process.stdin.flush()
          try:
            memory = psutil.Process(process.pid).memory_info().rss / (1024 * 1024)
          except psutil.NoSuchProcess:
            memory = 1

          start = time.perf_counter()
          process_output_data = process.communicate(input=judge_input)
          delta_time = time.perf_counter() - start

          output, error = [item.replace("\r\n", "\n").strip("\n") for item in process_output_data]

          if error:
            return JudgeResult(False, output, "IR", delta_time, 9999, error, 0, "You: (╯°□°）╯︵ ┻━┻ | It's ok my man, you can do it! Try again! ( ´･･)ﾉ(._.`)")

          try:
            return self.checker(output, judge_input, judge_output, accepted_point, delta_time, memory)
          except Exception as error:
            return JudgeResult(False, output, "IR", delta_time, 9999, "\n".join(traceback.format_exception(error)), 0, "Aight, what's wrong?")

        communication_thread = TomChienXuOJThread(target=judge)
        communication_thread.start()
        return_data = communication_thread.join(timeout=timeout)

        # filepaths = re.findall("File \"(.*\\.*\.py)\"", return_data.standard_error_result)
        # for filepath in filepaths:
        #   return_data.standard_error_result = return_data.standard_error_result.replace(filepath, os.path.basename(filepath))

        if communication_thread.is_alive():
          psutil_process_handled = psutil.Process(process.pid)
          for child in psutil_process_handled.children(recursive=True):
            child.terminate()
          process.terminate()
          communication_thread.join()
          return JudgeResult(False, "Unrequited", "TLE", timeout, 9999, f"Time Limit Exceeded! Runtime judge note: > {timeout}s!", 0, "/(ㄒoㄒ)/~~ Why :<")

        return return_data

      except Exception as error:
        return JudgeResult(False, "Unidentified Exception", "IR", 9999, 9999, "\n".join(traceback.format_exception(error)), 0, "(This can be judge's exception, may be not yours! You can create a ticket to be able to view this submission) We actually don't know why this happened tho! ¯\_(ツ)_/¯")

  def single_judge(self, input_file_name: str, output_file_name: str, accepted_point: Union[float, int] = 0.1, timeout: Union[float, int] = 1.0) -> JudgeResult:
    if input_file_name:
      with open(f"{PROBLEM_TESTCASE_ROOT_STORAGE}/{self.problem_code}/{input_file_name}", "r", encoding="utf-8") as input_:
        input_ = input_.read()
    else:
      input_ = None

    if output_file_name:
      with open(f"{PROBLEM_TESTCASE_ROOT_STORAGE}/{self.problem_code}/{output_file_name}", "r", encoding="utf-8") as output_:
        output_ = output_.read()
    else:
      output_ = None

    result = self.process(input_, output_, accepted_point, timeout)
    return result

  def close(self) -> None:
    self.judge_folder.cleanup()

  def __exit__(self) -> None:
    self.close()

from .custom_checker_template import line_by_line_token_standard_checker

class Judge:
  def __init__(self, name: str, description: str = "TomChienXuOJ's judge system.", socket_supported: bool = USE_SOCKETIO_EVENT, languages: List[str] = None, authentication: str = None, default_checker: Callable = standard_checker) -> None:
    self.name: str = name
    self.description: str = description
    self.socket_supported: bool = socket_supported
    self.authentication: str = authentication or str(uuid.uuid4())
    self.default_checker: Callable = line_by_line_token_standard_checker # default_checker
    self.judge_processes: Dict[str, JudgeProcess] = {}
    self.running: bool = False
    self.languages: List[str] = languages
    self.language_statuses: Dict[str, Any] = {}
    self.socketio: socketio.Client = None

    if self.languages:
      for language in self.languages:
        language_package = importlib.import_module(f"{LANGUAGE_EXECUTOR_ROOT_STORAGE}.{language}").Executor
        status = language_package.command in BYPASSED_DEFAULT_CMD_COMMANDS or shutil.which(language_package.command)
        self.language_statuses[language] = {
          "status": True,
          "uptime_since": int(datetime.datetime.now().timestamp()),
          "display_name": language_package.language_full_name
        } if status else {
          "status": False,
          "uptime_since": None,
          "display_name": language_package.language_full_name
        }

        logger.info(f"Judge '{name}': Started {'un' if not status else ''}successfully '{language}'.")

  def start(self) -> bool:
    self.running = True
    if self.socket_supported:
      self.socketio = socketio.Client(ssl_verify=SSL_VERIFY)
      self.socketio.connect(FULL_DOMAIN_WITH_SCHEME, wait_timeout=10)
      logger.info(f"Judge '{self.name}': SocketIO server started successfully.")
    logger.info(f"Judge '{self.name}': Started successfully.")
    return self.running

  def stop(self) -> bool:
    self.running = False
    self.judge_processes.clear()
    logger.info(f"Judge '{self.name}': Stopped successfully, cleared all running judge processes.")
    return self.running

  @property
  def status(self) -> bool:
    return self.running

  def pre_initialize(func: Callable) -> Any:
    def inner(self, *args, **kwargs) -> Any:
      if not self.status:
        raise Exception("This judge is not running!")

      programming_language = self.judge_processes[kwargs.get("judge_process_authentication", args[0])].programming_language
      if not self.language_statuses[programming_language]["status"]:
        raise Exception("This programming language is not available on this judge!")

      return func(self, *args, **kwargs)
    return inner

  def initialize_judging_process(self, problem_code: str, judge_type: str, programming_language: str, code: str, checker: Callable = None) -> str:
    if not self.status:
      return

    judge_process = JudgeProcess(self, problem_code, judge_type, programming_language, code, checker or self.default_checker)
    authentication = judge_process.authentication
    self.judge_processes[authentication] = judge_process
    return authentication

  @pre_initialize
  def execute_single_judging_process(self, judge_process_authentication: str, input_file: str, output_file: str, accepted_point: Union[float, int] = 0.1, timeout: Union[float, int] = 1.0, checker: Callable = None, close_folder: bool = False) -> Union[JudgeResult, Tuple[str]]:
    judge_process = self.judge_processes[judge_process_authentication]
    if checker:
      judge_process.checker = checker

    return_judge_data = judge_process.single_judge(input_file, output_file, accepted_point, timeout)

    if close_folder:
      self.close_judging_process(judge_process_authentication)

    return return_judge_data

  @pre_initialize
  def execute_all_judging_process(self, judge_process_authentication: str, timeout: Union[float, int] = 1.0) -> List[Union[JudgeResult, Tuple[str]]]:
    return_data = []
    problem_code = self.judge_processes[judge_process_authentication].problem_code
    problem_data = get_json_data(f"{PROBLEM_TESTCASE_ROOT_STORAGE}/{problem_code}/data.json")
    judge_data = problem_data.get("cases")

    custom_checker = None
    if problem_data.get("custom_checker"):
      temporary_directory = tempfile.TemporaryDirectory(prefix="TomChienXuOJQualified_", suffix=f"_CustomChecker_{problem_code}")
      with open(f"{JUDGE_SERVER_ROOT_STORAGE}/judge_result.py", "r", encoding="utf-8") as file:
        judge_result_header = file.read()

      with open(f"{temporary_directory.name}/custom_checker.py", "w", encoding="utf-8") as file:
        file.write(judge_result_header + "\n" + problem_data["custom_checker"])

      try:
        spec = importlib.util.spec_from_file_location("custom_checker", f"{temporary_directory.name}/custom_checker.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        custom_checker = module.check
      except:
        logging.warning(f"Custom checker of problem '{problem_code}' couldn't be loaded! Traceback to default checker.")

    if SAFE_FIRST_START_AFTER_COMPILING:
      self.execute_single_judging_process(judge_process_authentication, judge_data[0][0].get("input_file"), judge_data[0][0].get("output_file"), judge_data[0][0].get("point"), timeout, custom_checker)

    for batch in judge_data:
      batch_data = []
      for case in batch:
        judge_process = self.execute_single_judging_process(judge_process_authentication, case.get("input_file"), case.get("output_file"), case.get("point"), timeout, custom_checker)
        batch_data.append(judge_process.data)

        logger.info((judge_process.accepted_or_not, judge_process.status_code, judge_process.time, judge_process.memory, judge_process.point, judge_process.feedback))
        if self.socket_supported:
          self.socketio.emit("receiving_judge_feedback_from_judge", (judge_process_authentication, return_data + [batch_data]))

      return_data.append(batch_data)

    self.close_judging_process(judge_process_authentication)
    return return_data

  def close_judging_process(self, judge_process_authentication: str) -> None:
    self.judge_processes[judge_process_authentication].close()
    self.judge_processes.pop(judge_process_authentication)