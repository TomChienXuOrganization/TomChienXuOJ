from flask_socketio import join_room
from flask_socketio import leave_room
from . import socketio
from . import markdown

@socketio.on("join_room_submission")
def join_room_submission(submission_authentication: str):
  join_room(submission_authentication)

@socketio.on("leave_room_submission")
def leave_room_submission(submission_authentication: str):
  leave_room(submission_authentication)

@socketio.on("receiving_judge_feedback_from_judge")
def receiving_judge_feedback_from_judge(submission_authentication: str, data: list):
  socketio.emit("receiving_judge_feedback_from_server", data, room=submission_authentication)

@socketio.on("render_markdown")
def render_markdown(data: str) -> str:
  return markdown.convert(data)