from subprocess import call
from src.server import keep_alive

keep_alive()
call(["python3", "src/main_bot.py"])
