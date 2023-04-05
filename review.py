#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from os import environ
import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)  

class Review(db.Model):
    __tablename__ = 'review'

    reviewID = db.Column(db.Integer, primary_key=True)
    hawkerID = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    def json(self):
        dto = {
            'reviewID': self.reviewID,
            'hawkerID': self.hawkerID,
            'review': self.review,
            'timestamp': self.timestamp,
        }

        return dto

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
    

@app.route("/postreview", methods=['POST'])
def create_review():

    hawkerID = request.json.get('hawkerID', None)
    review = request.json.get('review', None)
    add_review = Review(hawkerID=hawkerID, review=review)
         
    try:

        db.session.add(add_review)
        db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating review. " + str(e)
            }
        ), 500
    
    print(json.dumps(add_review.json(), default=str)) # convert a JSON object to a string and print
    print()

    return jsonify(
        {
            "code": 201,
            "data": add_review.json()
        }
    ), 201

@app.route("/getreview/<int:hawkerID>")
def get_all_hawker(hawkerID):
    reviewlist = Review.query.filter_by(hawkerID=hawkerID).all()
    if len(reviewlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "reviews": [review.json() for review in reviewlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no reviews with this hawker."
        }
    ), 404


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage reviews ...")
    app.run(host='0.0.0.0', port=5004, debug=True)
