#!/usr/bin/python3
"""Write a script that starts a Flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    """landing page"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """display hbnb"""
    return "HBNB"


@app.route("/c/<text>")
def display_c(text):
    """display c followed by text"""
    text = text.replace("_", " ")
    return f"C {text}"


@app.route("/python/", defaults={"text": "is cool"})
@app.route("/python/<text>")
def display_python(text):
    text = text.replace("_", " ")
    return f"Python {text}"


@app.route("/number/<int:n>")
def display_number(n):
    if isinstance(n, int):
        return f"{n} is a number"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
