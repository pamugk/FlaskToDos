"""
This script runs the FlaskToDos application using a development server.
"""

from os import environ
from FlaskToDos import app
from FlaskToDos.database import init_db


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    init_db()
    app.run(HOST, PORT, debug=True)
