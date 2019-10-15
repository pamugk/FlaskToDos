"""
The flask application package.
"""

from flask import Flask


app = Flask(__name__)
app.secret_key = '6c131473-dcc5-4c44-9934-5526a9df4d02'

from FlaskToDos import views
from FlaskToDos.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()