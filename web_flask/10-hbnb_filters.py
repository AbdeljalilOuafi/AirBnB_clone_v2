#!/usr/bin/python3

#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template
from models import *
from models.state import State
from models.amenity import Amenity
from models import storage
app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def states_and_amenities():
    """display the states and cities listed in alphabetical order"""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    print(states)
    print(amenities)
    return render_template('10-hbnb_filters.html', states=states, amenities=amenities)


@app.teardown_appcontext
def close_dataB(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
