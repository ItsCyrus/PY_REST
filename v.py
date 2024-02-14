from incoming import PayloadValidator, validators

# Define the payload schema
payload_validator = PayloadValidator({
    "bookingdates": {
        "checkin": validators.All(
            validators.Required(),
            validators.String(),
            validators.Match(r'^\d{4}-\d{2}-\d{2}$')  # Match YYYY-MM-DD format
        ),
        "checkout": validators.All(
            validators.Required(),
            validators.String(),
            validators.Match(r'^\d{4}-\d{2}-\d{2}$')  # Match YYYY-MM-DD format
        )
    }
})

# Example payload
payload = {
    "bookingdates": {
        "checkin": "2018-01-01",
        "checkout": "2019-01-01"
    }
}

# Validate the payload
validation_result = payload_validator.validate(payload)

# Check validation result
if validation_result.is_valid():
    print("Payload is valid!")
else:
    print("Validation errors:")
    for error in validation_result.errors():
        print("-", error)
