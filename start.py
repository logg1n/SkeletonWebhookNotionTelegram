import subprocess

subprocess.Popen(["python", "server/flask.py"])
subprocess.Popen(["python", "telegram/bot.py"])
