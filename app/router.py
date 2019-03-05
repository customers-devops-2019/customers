import os
import sys
from flask import Flask, Response, jsonify, request, json, url_for
from flask_api import status    # HTTP Status Codes


# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

# Create Flask application
app = Flask(__name__)

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():

    return "<h1>Welcome to the Customers web service<h1>", status.HTTP_200_OK

######################################################################
# GET Customer by ID
######################################################################
@app.route('/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):

    return jsonify(data='You executed the read route'), status.HTTP_200_OK

######################################################################
# PUT Customer by ID
######################################################################
@app.route('/customers/<customer_id>', methods=['PUT'])
def put_customer(customer_id):

    return jsonify(data='You executed the update route'), status.HTTP_200_OK

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    print "Customer Service Starting..."
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
