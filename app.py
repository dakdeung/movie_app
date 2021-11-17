"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template

# from flask import make_response, abort
from config import db
from models import Movie, MovieSchema

# local modules
import config


# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")


# create a URL route in our application for "/"
@connex_app.route("/a")
def home():
#     """
#     This function just responds to the browser URL
#     localhost:5000/
#     :return:        the rendered template "home.html"
#     """
#     # return render_template("home.html")
    return "Hello"

if __name__ == '__main__':
    connex_app.run(host='localhost', port=5000, debug=True)