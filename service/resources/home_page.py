"""
This module contains routes without Resources
"""
from flask import render_template, make_response
from flask_restful import Resource
from service import app

######################################################################
# GET /
######################################################################
class HomePage(Resource):
    """ Resource fior the Home Page """
    def get(self):
        """ Returns the index page """
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200,headers)

# @app.route('/')
# def index():
#     """ Send back the home page """
#     return app.send_static_file('index.html')