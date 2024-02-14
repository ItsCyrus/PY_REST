import requests
from requests.exceptions import HTTPError
import json
from incoming import datatypes, PayloadValidator
import datetime as dt
from datetime import date, datetime

base = "https://restful-booker.herokuapp.com"


# Payload Validation
class REST_Validator(PayloadValidator):

    username = datatypes.String(error='username must be a string', required=False)
    firstname = datatypes.String(error='firstname must be a string', required=False)
    lastname = datatypes.String(error='lastname must be a string', required=False)
    totalprice = datatypes.Integer(error='totalprice must be an integer', required=False)
    depositpaid = datatypes.Boolean(error='depositpaid must be true or false', required=False)

    # bookingdates = datatypes.Function('validate_bookingdates', error='Release year must be in between 1800 and current year.', required=False)

    # @staticmethod
    # def validate_bookingdates(val, *args, **kwargs):
    #     if val is None:
    #         return False  # No payload provided, validation fails
    #     booking_dates = val.get('bookingdates')
    #     if booking_dates is None:
    #         return False  # Bookingdates field is missing or None
    #     try:
    #         checkin_date = datetime.strptime(booking_dates.get('checkin'), '%Y-%m-%d')
    #         checkout_date = datetime.strptime(booking_dates.get('checkout'), '%Y-%m-%d')
    #         return True
    #     except (ValueError, TypeError):
    #         return False


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
def get_booking(id):
    try:
        response = requests.get(f"{base}/booking/{id}", verify=False)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return handle_response(response)

# POST
def create_booking(booking_creation_data, headers):
    try:
        response = requests.post(f"{base}/booking", json=booking_creation_data, headers=headers, verify=False)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return handle_response(response)

# PUT
def update_booking(id, booking_update_data, headers):
    try:
        response = requests.put(f"{base}/booking/{id}", json=booking_update_data, headers=headers, verify=False)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return handle_response(response)
    
# PATCH
def patch_booking(id, booking_patch_data, headers):
    try:
        response = requests.patch(f"{base}/booking/{id}", json=booking_patch_data, headers=headers, verify=False)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return handle_response(response)
    
# DELETE
def delete_booking(id, headers):
    try:
        response = requests.delete(f"{base}/booking/{id}", headers=headers, verify=False)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return handle_response(response)

###############################################
    
# TEST
## Token generation
print()
print("Token generation")
username = "admin"
password = "password123"

t_data = {
    "username": username,
    "password": password
}

headers = {'Content-Type': 'application/json'}

result, errors = REST_Validator().validate(t_data)
assert result and errors is None, 'Validation failed.\n%s' % json.dumps(errors, indent=2)
if errors is None:
    print("Payload is valid!")
    token_q = get_token(t_data, headers)
    print(token_q.json())

token_val = 'token=' + json.loads(token_q.text)['token']
print(token_val)


## GET
print()
print("GET")
id = 2

get_q = get_booking(id)
print(get_q.json())


## POST
print()
print("POST")

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }

booking_creation_data = {
"firstname" : "Jim",
"lastname" : "Brown",
"totalprice" : 111,
"depositpaid" : True,
"bookingdates" : {
    "checkin" : "2018-01-01",
    "checkout" : "2019-01-01"
},
"additionalneeds" : "Breakfast"
}

result, errors = REST_Validator().validate(booking_creation_data)
assert result and errors is None, 'Validation failed.\n%s' % json.dumps(errors, indent=2)
if errors is None:
    print("Payload is valid!")
    post_q = create_booking(booking_creation_data, headers)
    print(post_q.json)


## PUT
print()
print("PUT")

id = 2
headers = {
    'Cookie': token_val,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }

booking_update_data = {
"firstname" : "Kat",
"lastname" : "Brown",
"totalprice" : 111,
"depositpaid" : True,
"bookingdates" : {
    "checkin" : "2018-01-01",
    "checkout" : "2019-01-01"
},
"additionalneeds" : "Lunch"
}

result, errors = REST_Validator().validate(booking_update_data)
assert result and errors is None, 'Validation failed.\n%s' % json.dumps(errors, indent=2)
if errors is None:
    print("Payload is valid!")
    put_q = update_booking(id, booking_update_data, headers)
    print(put_q.json())


## PATCH
print()
print("PATCH")

id = 2
headers = {
    'Cookie': token_val,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }

booking_patch_data = {
"firstname" : "Jimothy",
"lastname" : "Brown"
}

result, errors = REST_Validator().validate(booking_patch_data)
assert result and errors is None, 'Validation failed.\n%s' % json.dumps(errors, indent=2)
if errors is None:
    print("Payload is valid!")
    patch_q = patch_booking(id, booking_patch_data, headers)
    print(patch_q.json())


## DELETE
print()
print("DELETE")    

id = 1
headers = {
    'Cookie': token_val,
    'Content-Type': 'application/json'
    }

delete_q = delete_booking(id, headers)