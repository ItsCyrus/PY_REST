import requests
import json
from incoming import datatypes, PayloadValidator, validators
import datetime as dt
from datetime import datetime

# VALIDATION
class PersonValidator(PayloadValidator):

    username = datatypes.String(error='username must be a string', required=False)
    firstname = datatypes.String(error='firstname must be a string', required=False)
    lastname = datatypes.String(error='lastname must be a string', required=False)
    totalprice = datatypes.Integer(error='totalprice must be an integer', required=False)
    depositpaid = datatypes.Function('deposit_validation', error=('depositpaid can be true or false'), required=False)

    def deposit_validation(self, val, **kwargs):
        val = val.lower()
        if val == 'true' or val == 'false':
            return True
        return False
        
validator = PersonValidator()

# BOOKING CODE VALIDATION
bookingdate_validator = PayloadValidator({
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

# Validate the payload
validation_result = bookingdate_validator.validate(bookingdates)

# Check validation result
if validation_result.is_valid():
    print("Payload is valid!")
else:
    print("Validation errors:")
    for error in validation_result.errors():
        print("-", error)



base = "https://restful-booker.herokuapp.com"

# Creates a token for PUT and DELETE requests
def get_token(username, password, headers):
    data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(f"{base}/auth", json=data, headers=headers, verify=False)
    return response

# GET
def get_booking(**kwargs):
    params = {key: value for key, value in kwargs.items() if value is not None}
    response = requests.get(f"{base}/booking", params=params)

    if response.status_code == 200:
        return response
    else:
        print("Request failed with status code:", response.status_code)
        return None

# POST
def create_booking(booking_creation_data, headers):
    response = requests.post(f"{base}/booking", json=booking_creation_data, headers=headers)

    if response.status_code == 200:
        return response
    else:
        print("Request failed with status code:", response.status_code)
        return None

# PUT
def update_booking(id, booking_update_data, headers):
    response = requests.put(f"{base}/booking/{id}", json=booking_update_data, headers=headers)

    if response.status_code == 200:
        return response
    else:
        print("Request failed with status code:", response.status_code)
        return None
    
# PATCH
def patch_booking(id, booking_patch_data, headers):
    response = requests.patch(f"{base}/booking/{id}", json=booking_patch_data, headers=headers)

    if response.status_code == 200:
        return response
    else:
        print("Request failed with status code:", response.status_code)
        return None
    
# DELETE
def delete_booking(id, headers):
    response = requests.delete(f"{base}/booking/{id}", headers=headers)

    if response.status_code == 200:
        return response
    else:
        print("Request failed with status code:", response.status_code)
        return None

###############################################
    
# TEST
## Token generation
username = "admin"
password = "password123"
headers = {'Content-Type': 'application/json'}

token_q = get_token(username, password, headers)
print(token_q.json())


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

get_q = get_booking(**optional_params)
print(get_q.json())


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

post_q = create_booking(booking_creation_data, headers)
print(post_q.json())


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

put_q = update_booking(id, booking_update_data, headers)
print(put_q.json())


## PATCH
id = 1
headers = {
    'Cookie': token_q.text(),
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }

booking_update_data = {
"firstname" : "Jimothy",
"lastname" : "Brown"
}

patch_q = patch_booking(id, booking_update_data, headers)
print(patch_q.json())


## DELETE
id = 1
headers = {
    'Cookie': token_q.text(),
    'Content-Type': 'application/json'
    }

delete_q = delete_booking(id, headers)
print(delete_q.json())