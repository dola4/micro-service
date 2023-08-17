import requests

AUTHENTICATE_SERVICE_URL = "http://localhost:5001"
PROFIL_MANAGEMENT_SERVICE_URL = "http://localhost:5002"
REQUEST_SERVICE_URL = "http://localhost:5003"
NOTIFICATION_SERVICE_URL = "http://localhost:5004"

# Call the authenticate service to create a user
def create_user():
    create_user = {"email": "wash@example.com", "password": "123", "role": "student",
                   "name": "Matthieu",
                   "phone": "091827343",
                   "door": "12098",
                   "street": "Your Street",
                   "city": "City",
                   "country": "Country",
                   "postal_code": "12345",
                   "birth_date": "01/01/2000",
                   }
    response = requests.post(AUTHENTICATE_SERVICE_URL + "/register", json = create_user)
    print(response.json())

# Call the authenticate service to login a user
def login_user():
    login_user_info = {"email": "john@example.com", "password": "123"}
    response = requests.post(AUTHENTICATE_SERVICE_URL + "/login", json=login_user_info)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error with status code: {response.status_code}")
        print(response.text)



# Call the profil management service to get a profil
def get_profil():
    role = "admin"
    user_id = "64d0f9b69e77271250f4372e"
    response = requests.get(f"{PROFIL_MANAGEMENT_SERVICE_URL}/userprofile/{role}/{user_id}")
    if response.status_code == 200:  # OK
        print(response.json())
    else:
        print("Error:", response.status_code, response.text)



# Call the profil management service to update a profil
def update_profil():
    role = "admin"
    user_id = "64d0f9b69e77271250f4372e"
    
    update_data = {
        "user": {
            "email": "newemail@example.com"
        },
        "role_data": {
            "address": "123 New Street"
        }
    }
    
    response = requests.put(
        f"{PROFIL_MANAGEMENT_SERVICE_URL}/userprofile/{role}/{user_id}", 
        json=update_data
    )
    
    if response.status_code == 200:  # OK
        print(response.json())
    else:
        print("Error:", response.status_code, response.text)


##############################################################################################################

# Call the profil management service to delete a profil
def delete_profil():   
    role = "student"
    user_id = "64d1117b09ea5fdf789f1e33"

    response = requests.delete(
        f"{PROFIL_MANAGEMENT_SERVICE_URL}/userprofile/{role}/{user_id}",
    )
    if response.status_code == 200:  # OK
        print(response.json())
    else:
        print("Error:", response.status_code, response.text)


# Call the request service to create a request
def create_request():
    create_message = {"to": "john@example.com", 
                      "from": "john@example.com", 
                      "subject": "Test", 
                      "body": "Test", 
                      "file": "test.txt"
                }
    with open("test.txt", "rb") as f:
        files = {"file": f}
        response = requests.post(REQUEST_SERVICE_URL + "/requests", files = files, data = create_message)
    print(response.json())


# Call the request service to get a request
def get_request():
    get_message = {"role": "admin", "user_id": "cp123"}
    response = requests.get(REQUEST_SERVICE_URL + "/requests", json=get_message)
    print(response.json())


# Call the request service to delete a request
def delete_request():
    delete_message = {"role": "admin", "user_id": "cp123"}
    response = requests.delete(REQUEST_SERVICE_URL + "/requests", json=delete_message)
    print(response.json())


# call the request service to get all requests from a user
def get_all_requests():
    get_all_message = {"role": "admin", "user_id": "cp123"}
    response = requests.get(REQUEST_SERVICE_URL + "/user_requests", json=get_all_message)
    print(response.json())


# call the request service to delete all requests from a user
def delete_all_requests():
    delete_all_message = {"role": "admin", "user_id": "cp123"}
    response = requests.delete(REQUEST_SERVICE_URL + "/user_requests", json=delete_all_message)
    print(response.json())


# call the request service to delete all recieved requests from a user
def delete_all_recieved_requests():
    delete_all_recieved_message = {"role": "admin", "user_id": "cp123"}
    response = requests.delete_recieved(REQUEST_SERVICE_URL + "/user_requests", json=delete_all_recieved_message)
    print(response.json())

# call the notification service
def create_notification():
    create_notification = {"channel": "email", "message": "Paie your bills", "recipient": "john@example.com", }
    response = requests.post(NOTIFICATION_SERVICE_URL, json = create_notification)
    print(response.json())

