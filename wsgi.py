"""WSGI entrypoint for Gunicorn.

Production: `gunicorn --bind 0.0.0.0:8000 wsgi:app`
"""

from src.app import app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
