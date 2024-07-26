#!/usr/bin/python3
"""flask web application that lists states dynamiclly"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states_list")
def states_list():
    """ states list"""
    states_dict = storage.all(State)
    render_template("7-states_list.html", states_dict=states_dict)

@app.teardown_appcontext
def close_db():
    """ states list"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



