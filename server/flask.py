# flask.py
from flask import Flask

from server import webhook_routes
from database import init_db

app = Flask(__name__)
app.register_blueprint(webhook_routes)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
