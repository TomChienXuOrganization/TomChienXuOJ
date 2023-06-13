from __future__ import annotations

from languages.base import CompilingExecutor
from .judge_result import JudgeResult
from typing import *
import sys
import os
import importlib
import traceback
import subprocess
import json
import uuid
import tempfile
import logging
import threading
import traceback
import shutil
import psutil
import time
import datetime

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

from constants import PROBLEM_TESTCASE_ROOT_STORAGE
from constants import LANGUAGE_EXECUTOR_ROOT_STORAGE
from constants import FAKE_LANGUAGES

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

def a_plus_b_custom_checker(process_output: str, judge_input: str, judge_output: str, accepted_point: Union[float, int], time: float, memory: int) -> JudgeResult:
  """
    Case in point for 'A plus B' problem (Custom Judge)
    Imagine there are no judge outputs imported.
  """

  if process_output == sum(map(int, judge_input.split())):
    return JudgeResult(True, process_output, "AC", time, memory, "", accepted_point, "o(*￣▽￣*)ブ Brilliant boi :D")
  else:
    return JudgeResult(False, process_output, "WA", time, memory, "", 0, "o(TヘTo) Life...")

class JudgeProcess:
  def __init__(self, judger: Judge, problem_code: str, judge_type: str, programming_language: str, code: str, checker: Callable) -> None:
    self.language_package: CompilingExecutor = importlib.import_module(f"{LANGUAGE_EXECUTOR_ROOT_STORAGE}.{programming_language}").Executor
    self.judger: Judge = judger
    self.problem_code: str = problem_code
    self.judge_type: str = judge_type
    self.programming_language: str = programming_language
    self.authentication: str = str(uuid.uuid4())
    self.code: str = code
    self.checker: Callable = checker
    self.judge_folder: tempfile.TemporaryDirectory = tempfile.TemporaryDirectory(prefix="TomChienXuOJQualified_", suffix=f"_Judge_{self.judger.authentication}_{self.authentication}")
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
    with open(self.full_directory, "w", encoding="utf-8") as file:
      file.write(self.code)

    with subprocess.Popen(
      self.language_package.get_compile_command().replace("%original_file%", self.full_directory).replace("%output_file%", self.full_output_directory),
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      universal_newlines=True
    ) as compiling_process:
      output, error = [item.replace("\r\n", "\n").strip("\n") for item in compiling_process.communicate()]

      if compiling_process.returncode != 0:
        return False, JudgeResult(False, "An exception has occurred!", "RTE", 9999, 9999, error or output, 0, "The compiler is working fine, but your code isn't. (┬┬﹏┬┬)")
      else:
        return (True,)

  def process(self, judge_input: str, judge_output: str, accepted_point: Union[float, int] = 0.1, timeout: Union[float, int] = 1.0) -> JudgeResult:
    if not self.compilable:
      return self.compile_error

    judge_input: str = judge_input.replace("\r\n", "\n").strip("\n")

    command = [self.language_package.executable, self.full_output_directory] if self.language_package.executable else self.full_output_directory
    with subprocess.Popen(
      command,
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      universal_newlines=True
    ) as process:
      try:
        def judge():
          # process.stdin.write(judge_input)
          # process.stdin.flush()
          start = time.perf_counter()
          memory = psutil.Process(process.pid).memory_info().rss / (1024 * 1024)
          output, error = [item.replace("\r\n", "\n").strip("\n") for item in process.communicate(input=judge_input)]
          delta_time = time.perf_counter() - start

          if error:
            return JudgeResult(False, output, "IR", delta_time, 9999, error, 0, "You: (╯°□°）╯︵ ┻━┻ | It's ok my man, you can do it! Try again! ( ´･･)ﾉ(._.`)")

          return self.checker(output, judge_input, judge_output, accepted_point, delta_time, memory)

        communication_thread = TomChienXuOJThread(target=judge)
        communication_thread.start()
        return_data = communication_thread.join(timeout=timeout)

        if communication_thread.is_alive():
          process.terminate()
          communication_thread.join()
          return JudgeResult(False, "Unrequited", "TLE", timeout, 9999, f"Time Limit Exceeded! Runtime judge note: > {timeout}s!", 0, "/(ㄒoㄒ)/~~ Why :<")

        return return_data

      except Exception as error:
        return JudgeResult(False, "Unidentified Exception", "IR", 9999, 9999, "\n".join(traceback.format_exception(error)), 0, "(This can be judge's exception, may be not yours! You can create a ticket to be able to view this submission) We actually don't know why this happened tho! ¯\_(ツ)_/¯")

  def single_judge(self, input_file_name: str, output_file_name: str, accepted_point: Union[float, int] = 0.1, timeout: Union[float, int] = 1.0) -> JudgeResult:
    with (
      open(f"{PROBLEM_TESTCASE_ROOT_STORAGE}/{self.problem_code}/{input_file_name}", "r", encoding="utf-8") as input_,
      open(f"{PROBLEM_TESTCASE_ROOT_STORAGE}/{self.problem_code}/{output_file_name}", "r", encoding="utf-8") as output_
    ):
      input_, output_ = input_.read(), output_.read()

    result = self.process(input_, output_, accepted_point, timeout)
    return result

  def close(self) -> None:
    self.judge_folder.cleanup()

  def __exit__(self) -> None:
    self.close()

class Judge:
  def __init__(self, name: str, description: str = "TomChienXuOJ's judge system.", languages: List[str] = None, authentication: str = None, default_checker: Callable = standard_checker) -> None:
    self.name: str = name
    self.description: str = description
    self.authentication: str = authentication or str(uuid.uuid4())
    self.default_checker: Callable = default_checker
    self.judge_processes: Dict[str, JudgeProcess] = {}
    self.running: bool = False
    self.languages: List[str] = languages
    self.language_statuses: Dict[str, Any] = FAKE_LANGUAGES

    if self.languages:
      for language in self.languages:
        language_package = importlib.import_module(f"{LANGUAGE_EXECUTOR_ROOT_STORAGE}.{language}").Executor
        status = shutil.which(language_package.command)
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
    return self.running

  def stop(self) -> bool:
    self.running = False
    self.judge_processes.clear()
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
  def execute_single_judging_process(self, judge_process_authentication: str, input_file: str, output_file: str, accepted_point: Union[float, int] = 0.1, timeout: Union[float, int] = 1.0, close_folder: bool = False) -> Union[JudgeResult, Tuple[str]]:
    judge_process = self.judge_processes[judge_process_authentication]
    return_judge_data = judge_process.single_judge(input_file, output_file, accepted_point, timeout)

    if close_folder:
      self.close_judging_process(judge_process_authentication)

    return return_judge_data.data

  @pre_initialize
  def execute_all_judging_process(self, judge_process_authentication: str, timeout: Union[float, int] = 1.0) -> List[Union[JudgeResult, Tuple[str]]]:
    return_data = []
    with open(f"{PROBLEM_TESTCASE_ROOT_STORAGE}/{self.judge_processes[judge_process_authentication].problem_code}/data.json", "r") as file:
      judge_data = json.load(file)

    for batch in judge_data:
      batch_data = []
      for case in batch:
        judge_process = self.execute_single_judging_process(judge_process_authentication, case["input_file"], case["output_file"], case["point"], timeout)
        batch_data.append(judge_process)

        logger.info(judge_process)

      return_data.append(batch_data)

    self.close_judging_process(judge_process_authentication)
    return return_data

  def close_judging_process(self, judge_process_authentication: str) -> None:
    self.judge_processes[judge_process_authentication].close()
    self.judge_processes.pop(judge_process_authentication)