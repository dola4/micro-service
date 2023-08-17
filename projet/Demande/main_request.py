from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo, ObjectId
from werkzeug.exceptions import BadRequest
from werkzeug.datastructures import FileStorage
import os

app = Flask(__name__)
api = Api(app)

# Configure the connection to your MongoDB instance


app.config["MONGO_URI"] = "mongodb://localhost:27017/gedocs"
mongo = PyMongo(app)

# Directory for uploaded files
UPLOAD_DIRECTORY = "project/api_uploaded_files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

class RequestManagement(Resource):
    def post(self):
        # Create a new request
        # Parse the arguments
        parser = reqparse.RequestParser()
        parser.add_argument('to', type=str, help='To whom the request is addressed', required=True)
        parser.add_argument('from', type=str, help='From whom the request is sent', required=True)
        parser.add_argument('subject', type=str, help='Subject of the request', required=True)
        parser.add_argument('body', type=str, help='Body of the request', required=True)
        parser.add_argument('file', type=FileStorage, location='files')

        data = parser.parse_args()

        if data['file']:
            file = data['file']
            filename = os.path.join(UPLOAD_DIRECTORY, file.filename)
            file.save(filename)
            data['file'] = filename 

        mongo.db.requests.insert_one(data)

        return {'message': 'New request created!'}
        

    def get(self, request_id):
        # Get a specific request
        request = mongo.db.requests.find_one({'_id': ObjectId(request_id)})
        
        if not request:
            raise BadRequest('Request does not exist')

        return request
    
    def delete(self, request_id):
        # Delete a specific request
        mongo.db.requests.delete_one({'_id': ObjectId(request_id)})
        return {'message': 'Request deleted!'}




class RequestByUser(Resource):
    def get(self, user_id):
        # Get all requests for a specific user
        requests_send = list(mongo.db.requests.find({'from': user_id}))
        requests_received = list(mongo.db.requests.find({'to': user_id}))
        return  {'requests_send': requests_send, 'requests_received': requests_received}
    
    def delete(self, user_id):
        # Delete all requests for a specific user
        mongo.db.requests.delete_many({'from': user_id})
        return {'message': 'All sent requests deleted!'}



api.add_resource(RequestByUser, '/user_requests/<string:user_id>')
api.add_resource(RequestManagement, '/requests', '/requests/<string:request_id>')

if __name__ == '__main__':
    app.run(debug=True, port=5003)
