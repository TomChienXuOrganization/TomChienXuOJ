import datetime

FAKE_LANGUAGES_STATUS = False

MAX_FILE_CONTENT_SIZE = 100 # Megabytes

DATABASE_FOLDER = "databases"
DATABASE_FILENAME = "database"

PROBLEM_TESTCASE_ROOT_STORAGE = "problems"
LANGUAGE_EXECUTOR_ROOT_STORAGE = "languages"

FAKE_LANGUAGES = {
  "BRAINFUCK": {
    "status": True,
    "uptime_since": int(datetime.datetime.now().timestamp()),
    "display_name": "Brainfuck"
  },
  "CPP17": {
    "status": True,
    "uptime_since": int(datetime.datetime.now().timestamp()),
    "display_name": "C++ 17"
  }, 
  "CPPTHEMIS": {
    "status": True,
    "uptime_since": int(datetime.datetime.now().timestamp()),
    "display_name": "C++ (Themis)"
  },
  "CPP17": {
    "status": True,
    "uptime_since": int(datetime.datetime.now().timestamp()),
    "display_name": "C++ 17"
  }, 
  "PAS": {
    "status": True,
    "uptime_since": int(datetime.datetime.now().timestamp()),
    "display_name": "Pascal 3.2.2"
  }, 
  "PASTHEMIS": {
    "status": True,
    "uptime_since": int(datetime.datetime.now().timestamp()),
    "display_name": "Pascal (Themis)"
  }, 
  "JAVA": {
    "status": True,
    "uptime_since": int(datetime.datetime.now().timestamp()),
    "display_name": "Java 19"
  }, 
  "C": {
    "status": True,
    "uptime_since": int(datetime.datetime.now().timestamp()),
    "display_name": "C"
  }, 
  "C#": {
    "status": True,
    "uptime_since": int(datetime.datetime.now().timestamp()),
    "display_name": "C#"
  }, 
  "TEXT": {
    "status": True,
    "uptime_since": int(datetime.datetime.now().timestamp()),
    "display_name": "TEXT"
  }, 
  "SCRATCH": {
    "status": True,
    "uptime_since": int(datetime.datetime.now().timestamp()),
    "display_name": "Scratch"
  }
} if FAKE_LANGUAGES_STATUS else {}