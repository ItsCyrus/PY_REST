import requests
from requests.exceptions import HTTPError
import json
from incoming import datatypes, PayloadValidator, validators
import datetime as dt
from datetime import datetime


base = "https://restful-booker.herokuapp.com"


# Payload Validation
class PersonValidator(PayloadValidator):

    username = datatypes.String(error='username must be a string', required=False)
    firstname = datatypes.String(error='firstname must be a string', required=False)
    lastname = datatypes.String(error='lastname must be a string', required=False)
    totalprice = datatypes.Integer(error='totalprice must be an integer', required=False)
    depositpaid = datatypes.Function('deposit_validation', error=('depositpaid can be true or false'), required=False)
    bookingdates = PayloadValidator({
        "bookingdates": {
            "checkin": validators.All(
                validators.Required(),
                validators.String(),
                validators.Match(r'^\d{4}-\d{2}-\d{2}$')
            ),
            "checkout": validators.All(
                validators.Required(),
                validators.String(),
                validators.Match(r'^\d{4}-\d{2}-\d{2}$')
            )
        }
    })

validator = PersonValidator()


def handle_response(response):
    if response.status_code == 200:
        return response
    elif response.status_code == 404:
        print("404 Error: Resource not found")
    elif response.status_code == 400:
        print("400 Error: Bad request")
    elif response.status_code == 401:
        print("401 Error: Unauthorized")
    elif response.status_code == 403:
        print("403 Error: Forbidden")
    elif response.status_code == 500:
        print("500 Error: Internal Server Error")
    else:
        print("Error:", response.status_code)


# Creates a token for PUT and DELETE requests
def get_token(data, headers):
    try:
        response = requests.post(f"{base}/auth", json=data, headers=headers, verify=False)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return handle_response(response)


# GET
def get_booking(**kwargs):
    params = {key: value for key, value in kwargs.items() if value is not None}
    try:
        response = requests.get(f"{base}/booking", params=params)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return handle_response(response)

# POST
def create_booking(booking_creation_data, headers):
    try:
        response = requests.post(f"{base}/booking", json=booking_creation_data, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return handle_response(response)

# PUT
def update_booking(id, booking_update_data, headers):
    try:
        response = requests.put(f"{base}/booking/{id}", json=booking_update_data, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return handle_response(response)
    
# PATCH
def patch_booking(id, booking_patch_data, headers):
    try:
        response = requests.put(f"{base}/booking/{id}", json=booking_patch_data, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return handle_response(response)
    
# DELETE
def delete_booking(id, headers):
    try:
        response = requests.delete(f"{base}/booking/{id}", headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return handle_response(response)

###############################################
    
# TEST
## Token generation
username = "admin"
password = "password123"

t_data = {
    "username": username,
    "password": password
}

headers = {'Content-Type': 'application/json'}

validation_result = validator.validate(t_data)
if validation_result.is_valid():
    print("Payload is valid!")
    token_q = get_token(t_data, headers)
    print(token_q.json())
else:
    print("Validation errors:")
    for error in validation_result.errors():
        print("-", error)


## GET
firstname = None
lastname = None
checkin = None
checkout = None

optional_params = {
    "firstname": firstname,
    "lastname": lastname,
    "checkin": checkin,
    "checkout": checkout
}

validation_result = validator.validate(optional_params)
if validation_result.is_valid():
    print("Payload is valid!")
    get_q = get_booking(**optional_params)
    print(get_q.json())
else:
    print("Validation errors:")
    for error in validation_result.errors():
        print("-", error)


## POST
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }

booking_creation_data = {
"firstname" : "Jim",
"lastname" : "Brown",
"totalprice" : 111,
"depositpaid" : "true",
"bookingdates" : {
    "checkin" : "2018-01-01",
    "checkout" : "2019-01-01"
},
"additionalneeds" : "Breakfast"
}

validation_result = validator.validate(booking_creation_data)
if validation_result.is_valid():
    print("Payload is valid!")
    post_q = create_booking(booking_creation_data, headers)
    print(post_q.json())
else:
    print("Validation errors:")
    for error in validation_result.errors():
        print("-", error)


## PUT
id = 1
headers = {
    'Cookie': token_q.text(),
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }

booking_update_data = {
"firstname" : "Kat",
"lastname" : "Brown",
"totalprice" : 111,
"depositpaid" : "true",
"bookingdates" : {
    "checkin" : "2018-01-01",
    "checkout" : "2019-01-01"
},
"additionalneeds" : "Breakfast"
}

validation_result = validator.validate(booking_update_data)
if validation_result.is_valid():
    print("Payload is valid!")
    put_q = update_booking(id, booking_update_data, headers)
    print(put_q.json())
else:
    print("Validation errors:")
    for error in validation_result.errors():
        print("-", error)


## PATCH
id = 1
headers = {
    'Cookie': token_q.text(),
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }

booking_patch_data = {
"firstname" : "Jimothy",
"lastname" : "Brown"
}

validation_result = validator.validate(booking_patch_data)
if validation_result.is_valid():
    print("Payload is valid!")
    patch_q = patch_booking(id, booking_patch_data, headers)
    print(patch_q.json())
else:
    print("Validation errors:")
    for error in validation_result.errors():
        print("-", error)


## DELETE
id = 1
headers = {
    'Cookie': token_q.text(),
    'Content-Type': 'application/json'
    }

delete_q = delete_booking(id, headers)
print(delete_q.json())