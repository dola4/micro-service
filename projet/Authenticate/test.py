import requests
import json

""" url = "http://127.0.0.1:5000/register" 
data = {
    "email": "test@example.com",
    "password": "password",
    "role": "student",
    "door": "123",
    "street": "street",
    "city": "city",
    "state": "state",
    "country": "country",
    "zip": "zip",
    "lastName": "lastName",
    "firstName": "firstName",
    "birthDate": "birthDate",
    "phone": "phone",    
}
headers = {'Content-type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)
print("HTTP Status Code:", response.status_code)
print("Raw Response:", response.text)

print(response.json()) """

url = "http://127.0.0.1:5000/login"
data = {
    "email": "test@example.com",
    "password": "password",
}
headers = {'Content-type': 'application/json'}
response = requests.post(url, data=json.dumps(data), headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print("An error occurred: HTTP", response.status_code)
    print(response.text)

