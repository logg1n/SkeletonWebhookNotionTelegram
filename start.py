import subprocess

subprocess.Popen(["python", "server/flask.py"])
subprocess.Popen(["python", "telegram_bot/bot.py"])
