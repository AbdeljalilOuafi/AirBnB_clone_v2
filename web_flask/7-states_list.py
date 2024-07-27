#!/usr/bin/python3
""" module doc """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ render all states from db """
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def close(error):
    """ clean up and close db connection """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
