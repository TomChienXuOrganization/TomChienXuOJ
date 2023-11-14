import datetime
from . import TomChienXuOJ_SupportDefaultItems
from helpers import TimezoneMixin
from pages import database
from sqlalchemy.sql import func, expression

content_custom_checker = """<div class="alert alert-warning">
By the time this page is being written, our system only support custom checker by Python 3.11 and not-an-interactive judge. Otherwise feel free to use the checker. Besides, we also provide many our own custom coded judges with presets, yay.
</div>

First of all, setup a function (must be named `check`):

```py
def check(process_output, judge_input, judge_output, accepted_point, time, memory):
  ...
```

- `process_output` is the output after the execution the code of the author with `judge_input`.
- `judge_input`: Judge's input, provided through file or *Standard Input Stream Line*.
- `judge_input`: Judge's output, gotten through file or *Standard Output Stream Line*.
- `accepted_point`: Points granted when [verdict:AC] a problem (can be partial).
***Case in point:** The author of the code has successfully completed all tokens, then they get all the points; otherwise, they get only $5$ out of $10$ tokens right, then they get `accepted_point * 5 / 10`.
- `time`: Time of the execution (second).
- `memory`: Memory usage of the execution [<i>currently not usable</i>] (Megabyte).

This function must return a `JudgeResult` object, this class will automatically be appended when the custom judge is initialized:

```py
class JudgeResult:
  def __init__(self, accepted_or_not: bool, return_result: str, status_code: str, time: float, memory: int, standard_error_result: str = "", point: float = 0, feedback: str = "") -> None:
    self.accepted_or_not: bool = accepted_or_not
    self.return_result: str = return_result[:20]
    self.status_code: str = status_code
    self.standard_error_result: str = standard_error_result
    self.point: float = point
    self.feedback: str = feedback
    self.time: float = time
    self.memory: int = memory

  @property
  def status(self):
    return self.accepted_or_not

  @property
  def data(self):
    return {
      "accepted_or_not": self.accepted_or_not,
      "return_result": self.return_result,
      "status_code": self.status_code,
      "standard_error_result": self.standard_error_result,
      "point": self.point,
      "feedback": self.feedback,
      "time": self.time,
      "memory": self.memory
    }

  def get_data(self):
    return self.data
```

The `JudgeResult` object will contain:

- `accepted_or_not`: True or False, whether the case was acceptable or not.
- `return_result`: Just use the `process_output` for short, capped at the $20^{th}$ letter for WebSocket system compatibility.
- `status_code`: Visit [this page](/flat/status_codes) for more information.
- `standard_error_result`: `STDERR`, if it exists, tho. If you type some other shit in here, it will become a feedback box, without visibility ;-;
- `point`: Aforementioned.
- `time`: Aforementioned.
- `memory`: Aforementioned.

Some examples of our code for custom checker:

**\\*Note:** *Remember to change the name of the function into `check` or use `check` as a new name for this function*.

```py
check = a_plus_b_custom_checker
```

- Custom checker for [A Plus B](/p/aplusb):

```py
def a_plus_b_custom_checker(process_output: str, judge_input: str, judge_output: str, accepted_point: Union[float, int], time: float, memory: int) -> JudgeResult:
  \"""
    Case in point for 'A plus B' problem (Custom Judge)
    Imagine there are no judge outputs imported.
  \"""

  if int(process_output) == sum(map(int, judge_input.split())):
    return JudgeResult(True, process_output, "AC", time, memory, "", accepted_point, "o(*￣▽￣*)ブ Brilliant boi :D")
  else:
    return JudgeResult(False, process_output, "WA", time, memory, "", 0, "o(TヘTo) Life...")
```

- Custom checker for [Tempura Tournament 2023 - Đồ thị hàm số](/p/tempura_t23_dothihamso):

```py
def hnoj_graph1_custom_checker(process_output: str, judge_input: str, judge_output: str, accepted_point: Union[float, int], time: float, memory: int) -> JudgeResult:
  \"""
  The approximation must not be over 10^{-6}.
  \"""
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
```

- Line-by-line checker:

```py
def ordinal(n: int) -> str:
  if 11 <= (n % 100) <= 13:
    suffix = "th"
  else:
    suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
  return f"{n}-{suffix}"

def line_by_line_token_standard_checker(process_output, judge_input, judge_output, accepted_point, time, memory):
  judge_output = judge_output.rstrip("\\r\\n").split("\\n")
  process_output = process_output.rstrip("\\r\\n").split("\\n")

  if len(judge_output) != len(process_output):
    return JudgeResult(False, process_output, "WA", time, memory, "", 0, "Wrongly tokenized! Your output length (line-by-line) does not match ours!")

  for index in range(len(judge_output)):
    if judge_output[index] != process_output[index]:
      return JudgeResult(False, process_output, "WA", time, memory, "", 0, f"Wrongly comparison on the <b>{ordinal(index + 1)}</b> token!")

  return JudgeResult(True, process_output, "AC", time, memory, "", accepted_point, f"Correct answers. <b>{len(judge_output)}</b> token(s) has been returned!")
```
"""

content_status_codes = """> ##### The contents of this flat page are based on:
 - Don Mill's Online Judge ([here](https://dmoj.ca/about/codes))
 - VNOJ: VNOI Online Judge ([here](https://oj.vnoi.info/faq))
 - Luyencode Online Judge ([here](https://luyencode.net/faq))
>
> We appreciate your contributions, thanks!

This page lists all status codes encountered on the <b class="rgb">TomChienXuOJ</b> and their descriptions. It should be noted that it is possible for a case to be given multiple status codes (indeed, this is usually the case for non-[verdict:AC] verdicts), in which case the one with the highest priority will be displayed. This page lists status codes in order of increasing priority.

<div class="table-responsive">
  <table class="table-sm table-striped table table-hover table-bordered">
    <thead class="table-dark">
      <tr>
        <th scope="col" class="col-sm-3">Status Code</th>
        <th scope="col" class="col-sm-1">Abbreviation Form</th>
        <th scope="col" class="col-sm">Explanation</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Accepted</b></td>
        <td class="text-center">[verdict:AC]</td>
        <td>Your program passed testing! In some cases, this may be accompanied with additional feedback from the grader.</td>
      </tr>
      <tr>
        <td><b>Wrong Answer</b></td>
        <td class="text-center">[verdict:WA]</td>
        <td>Your program did not crash while executing, but the output it produced was wrong. As for <b class="text-success">AC</b>, this may be accompanied with additional feedback stating what you did wrong.</td>
      </tr>
      <tr>
        <td><b>Runtime Error/Exception</b></td>
        <td class="text-center">[verdict:RTE]</td>
        <td>Your program caused a runtime error to occur. This will only occur for native languages like <b>C</b> or <b>C++</b>. We map many common <b class="text-secondary">RTE</b>s to more useful descriptions, described below in this page.</td>
      </tr>
      <tr>
        <td><b>Invalid Return</b></td>
        <td class="text-center">[verdict:IR]</td>
        <td>Your program returned with a non-zero exit code (if you're not using a native language like <b>C++</b>, then it crashed). For languages like <b>Python</b> or <b>Java</b>, this will typically be accompanied with the name of the exception your program threw (<i>Case in point</i>: <code>NameError</code> or <code>java.lang.NullPointerException</code>, respectively).</td>
      </tr>
      <tr>
        <td><b>Output Limitation Exceeded</b></td>
        <td class="text-center">[verdict:OLE]</td>
        <td>Your program outputted too much data to <code>stdout</code> (<i>Standard Output Stream Line</i>), typically over <b>$256$ Megabytes</b> (though some problems may have custom - generally larger - constraints).</td>
      </tr>
      <tr>
        <td><b>Memory Limitation Exceeded</b></td>
        <td class="text-center">[verdict:MLE]</td>
        <td>Your program ran out of memory. Sometimes, this might manifest itself as an [verdict:RTE] with <code>segmentation fault</code> or <code>std::bad_alloc</code>.</td>
      </tr>
      <tr>
        <td><b>Time Limitation Exceeded</b></td>
        <td class="text-center">[verdict:TLE]</td>
        <td>Your program took too long to execute.</td>
      </tr>
      <tr>
        <td><b>Internal Error</b></td>
        <td class="text-center">[verdict:IE]</td>
        <td>If you see this, it means either the judge encountered an error or the problem-setter's configuration is incorrect. Administrators get notified of every internal error by email, and as such there is no need to do anything else - [verdict:IE]s will typically be resolved within $24$ hours (<i>or not, who knows (ﾉ*･ω･)ﾉ</i>).</td>
      </tr>
    </tbody>
  </table>
</div>
"""

class FlatPage(database.Model, TimezoneMixin, TomChienXuOJ_SupportDefaultItems):
  default_item_headers = ["page_code", "title", "content"]
  default_items = [
    ["custom_checker", "Everything you need to know to setup a custom checker", content_custom_checker],
    ["status_codes", "Status codes and Explanations (with notes, too)", content_status_codes]
  ]

  id = database.Column(database.Integer, primary_key=True, unique=True)
  page_code = database.Column(database.String, unique=True)
  regex_highlighter = database.Column(database.String)
  author_id = database.Column(database.Integer, database.ForeignKey("user.id"))
  title = database.Column(database.String, nullable=False)
  time = database.Column(database.DateTime(timezone=True), server_default=func.now())
  content = database.Column(database.Text, nullable=False)
  visibility = database.Column(database.Boolean, server_default=expression.true())

  def __repr__(self):
    return f"{self.id}: {self.title}"

  @property
  def time_timezone(self):
    return self.convert_time_as_timezone(self.time)