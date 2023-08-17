from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
from bson.json_util import dumps
import json


app = Flask(__name__)
api = Api(app)

# Configure the connection to your MongoDB instance
app.config["MONGO_URI"] = "mongodb://localhost:27017/gedocs"
mongo = PyMongo(app)

def jsonify_mongo(obj):
    return json.loads(dumps(obj))

class Register(Resource):
    def post(self):
        # Parse the arguments
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='Email address to create user')
        parser.add_argument('password', type=str, help='Password to create user')
        parser.add_argument('role', type=str, help='Role of the user')
        parser.add_argument('door', type=str, help='Door number')
        parser.add_argument('street', type=str, help='Street')
        parser.add_argument('city', type=str, help='City')
        parser.add_argument('state', type=str, help='State')
        parser.add_argument('country', type=str, help='Country')
        parser.add_argument('zip', type=str, help='Zip code')
        parser.add_argument('lastName', type=str, help='Last name')
        parser.add_argument('firstName', type=str, help='First name')
        parser.add_argument('birthDate', type=str, help='Birth date')
        parser.add_argument('phone', type=str, help='Phone number')
        parser.add_argument('num_employees', type=str, help='Number of employees')
        parser.add_argument('experience_years', type=str, help='Experience years')

        data = parser.parse_args()

        if data['email'] in [x for x in [x['email'] for x in json.loads(dumps(mongo.db.users.find()))]]:
            return {'message': 'User already exists'}, 400
        else:
            # Insert the user in the database
            user_id = mongo.db.users.insert_one({
                'email': data['email'],
                'password': data['password'],
                'role': data['role'],  # 'admin' or 'student'
            }).inserted_id

            user_adress_id = mongo.db.addresses.insert_one({
                'user_id': user_id,
                'door': data['door'],
                'street': data['street'],
                'city': data['city'],
                'state': data['state'],
                'country': data['country'],
                'zip': data['zip'],
            }).inserted_id

            if data['role'] == 'student':
                mongo.db.students.insert_one({
                    'user_id': user_id,
                    'address': user_adress_id,
                    'lastName': data['lastName'],
                    'firstName': data['firstName'],
                    'birthDate': data['birthDate'],
                    'phone': data['phone']
                }).inserted_id

            elif data['role'] == 'admin':
                mongo.db.admins.insert_one({
                    'user_id': user_id,
                    'address': user_adress_id,
                    'num_employees': data['num_employees'],
                    'experience_years': data['experience_years'],
                }).inserted_id

            return {'message': 'Registered successfully'}, 200


class Login(Resource):
    def post(self):
        # Get the request data
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='User email address to login use')
        parser.add_argument('password', type=str, help='User password to login use')
        data = parser.parse_args()

        # Check if the user exists
        user = mongo.db.users.find_one({"email": data['email']})

        if not user:
            return {'message': 'User does not exist'}, 400

        # Check if the password is correct
        if not user['password'] == data['password']:
            return {'message': 'Wrong password'}, 400

        # Fetch the corresponding role data
        role_data = None
        if user['role'] == 'admin':
            role_data = mongo.db.admins.find_one({"user_id": user['_id']})
        elif user['role'] == 'student':
            role_data = mongo.db.students.find_one({"user_id": user['_id']})

        # Fetch the address data
        address = mongo.db.addresses.find_one({"user_id": user['_id']})

        # Return the user data
        return {"data" : jsonify_mongo({
            "user": user,
            "role_data": role_data,
            "address": address
        }), 'message': 'Logged in successfully'}, 200


api.add_resource(Register, '/register')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
