from typing import Union
from .judge_result import JudgeResult

def ordinal(n: int) -> str:
  if 11 <= (n % 100) <= 13:
    suffix = "th"
  else:
    suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
  return f"{n}-{suffix}"

def a_plus_b_custom_checker(process_output: str, judge_input: str, judge_output: str, accepted_point: Union[float, int], time: float, memory: int) -> JudgeResult:
  """
    Case in point for 'A plus B' problem (Custom Judge)
    Imagine there are no judge outputs imported.
  """

  if process_output == sum(map(int, judge_input.split())):
    return JudgeResult(True, process_output, "AC", time, memory, "", accepted_point, "o(*￣▽￣*)ブ Brilliant boi :D")
  else:
    return JudgeResult(False, process_output, "WA", time, memory, "", 0, "o(TヘTo) Life...")

def hnoj_graph1_custom_checker(process_output: str, judge_input: str, judge_output: str, accepted_point: Union[float, int], time: float, memory: int) -> JudgeResult:
  """
  The approximation must not be over 10^{-6}.
  """
  judge_output = judge_output.split(" ")
  process_output = process_output.split(" ")

  wrong_answer = JudgeResult(False, process_output, "WA", time, memory, "", 0, "(≧﹏≦) Life doesn't always operate like the way we want! Be strong!")
  correct_answer = JudgeResult(True, process_output, "AC", time, memory, "", accepted_point, "o(*￣▽￣*)ブ Brilliant boi :D")

  if process_output[0] != judge_output[0]:
    return wrong_answer

  if process_output[0] == judge_output[0] == "Intersect":
    if abs(float(process_output[1]) - float(judge_output[1])) > 10**(-4) or abs(float(process_output[2]) - float(judge_output[2])) > 10**(-4):
      return wrong_answer

  return correct_answer

def line_by_line_token_standard_checker(process_output, judge_input, judge_output, accepted_point, time, memory):
  original_output = process_output

  judge_output = judge_output.rstrip("\r\n").split("\n") if judge_output else None
  process_output = process_output.rstrip("\r\n").split("\n") if process_output else None

  if len(judge_output) != len(process_output):
    return JudgeResult(False, original_output, "WA", time, memory, "", 0, "Wrongly tokenized! Your output length (line-by-line) does not match ours!")

  for index in range(len(judge_output)):
    if judge_output[index] != process_output[index]:
      return JudgeResult(False, original_output, "WA", time, memory, "", 0, f"Wrongly comparison on the <b>{ordinal(index + 1)}</b> token!")

  return JudgeResult(True, original_output, "AC", time, memory, "", accepted_point, f"Correct answers. <b>{len(judge_output)}</b> token(s) has been returned!")