from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from function import send_sms, send_email, send_whatsapp

app = Flask(__name__)
api = Api(app)

class NotificationService(Resource):
    def post(self):
        # Parse the arguments
        parser = reqparse.RequestParser()
        parser.add_argument('channel', type=str, help='Channel to send the notification', required=True)
        parser.add_argument('message', type=str, help='Message of the notification', required=True)
        parser.add_argument('recipient', type=str, help='Recipient of the notification', required=True)

        data = parser.parse_args()

        # Send the notification
        if data['channel'] == 'sms':
            send_sms(data['recipient'], data['message'])
        elif data['channel'] == 'email':
            send_email(data['recipient'], data['message'])
        elif data['channel'] == 'whatsapp':
            send_whatsapp(data['recipient'], data['message'])
        else:
            return {'message': 'Invalid notification channel'}, 400

        return {'message': 'Notification sent!'}

api.add_resource(NotificationService, '/notifications')

if __name__ == '__main__':
    app.run(debug=True, port=5004)
