
from flask_pymongo import PyMongo
import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from bson.json_util import dumps, loads
from bson.objectid import ObjectId


app = Flask(__name__)
api = Api(app)

# Configure the connection to your MongoDB instance
app.config["MONGO_URI"] = "mongodb://localhost:27017/gedocs"
mongo = PyMongo(app)


class UserProfile(Resource):
    def get(self, role, user_id):
        # Fetch the user data
        try:
            user_id = ObjectId(user_id)
        except:
            return {'message': 'Invalid user ID format'}, 400

        user = mongo.db.users.find_one({"_id": user_id})

        # Fetch the user data
        user = mongo.db.users.find_one({"_id": user_id})

        if not user:
            return {'message': 'User does not exist'}, 400

        # Fetch the corresponding role data
        role_data = None
        if role == 'admin':
            admin = mongo.db.admins.find_one({"user_id": user_id})
            all_students = list(mongo.db.students.find())
            all_adresses = list(mongo.db.adresses.find())
            role_data = {
                'admin': admin,
                'all_students': all_students,
                'all_adresses': all_adresses
            }

        elif role == 'student':
            role_data = mongo.db.students.find_one({"user_id": user_id})

        if not role_data:
            return {'message': 'Role data does not exist'}, 400

        # Return the user and role data
        return jsonify(json.loads(dumps({'user': user, 'role_data': role_data})))




    def put(self, role, user_id):

        try:
            user_id = ObjectId(user_id)
        except:
            return {'message': 'Invalid user ID format'}, 400
        # Get the request data
        data = request.get_json()

        # Update the user data
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {'$set': data['user']}
        )

        # Update the corresponding role data
        if role == 'admin':
            mongo.db.admins.update_one(
                {"user_id": ObjectId(user_id)},
                {'$set': data['role_data']}
            )
        elif role == 'student':
            mongo.db.students.update_one(
                {"user_id": ObjectId(user_id)},
                {'$set': data['role_data']}
            )

        return {'message': 'Profile updated successfully'}


    def delete(self, role, user_id):

        try:
            user_id = ObjectId(user_id)
        except:
            return {'message': 'Invalid user ID format'}, 400
        
        # Delete the user adress
        mongo.db.adresses.delete_one({"user_id": ObjectId(user_id)})

        # Delete the user data
        mongo.db.users.delete_one({"_id": ObjectId(user_id)})

        # Delete the corresponding role data
        if role == 'admin':
            mongo.db.admins.delete_one({"user_id": ObjectId(user_id)})
            return {'message': 'Profile deleted successfully'}

        elif role == 'student':
            mongo.db.students.delete_one({"user_id": ObjectId(user_id)})
            return {'message': 'Profile deleted successfully'}
        

        

api.add_resource(UserProfile, '/userprofile/<string:role>/<string:user_id>')



if __name__ == '__main__':
    app.run(debug=True, port=5002)
