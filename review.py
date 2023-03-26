#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from os import environ
import requests


app = Flask(__name__)


CORS(app)  


@app.route("/review/<int:pageID>")
def get_facebook_ratings(pageID):
    access_token = 'EABT6fmwJn4UBADarYUHenltvYCBIJkWqybWu3WI1imR9XlRbBs4M7aXgiNot9ndKaCwE3uRZA7wSdkZA5PVQLEfC9HPyAcAXK1u7sFMNTqvp5gv5uiKZBxJEZCCZAaBStognqgWtcpDKAyWBxkl0Yii5G4OLv7rtrAEZCPm8PMx1kAzYJ9XzIk'
    url = 'https://graph.facebook.com/v16.0/'+ str(pageID) +'/ratings?access_token={}'.format(access_token)
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if one occurred
        return jsonify(response.json())
    except requests.exceptions.HTTPError as error:
        return jsonify({'error': str(error)})

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
    app.run(host='0.0.0.0', port=5005, debug=True)
