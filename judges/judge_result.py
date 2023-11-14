class JudgeResult:
  def __init__(self, accepted_or_not: bool, return_result: str, status_code: str, time: float, memory: int, standard_error_result: str = "", point: float = 0, feedback: str = "") -> None:
    self.accepted_or_not: bool = accepted_or_not
    self.return_result: str = str(return_result)[:50].rstrip("\n") + "\n..." if len(str(return_result)) > 50 else str(return_result)
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
