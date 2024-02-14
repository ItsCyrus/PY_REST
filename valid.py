import json
from incoming import datatypes, PayloadValidator

class PersonValidator(PayloadValidator):

    name = datatypes.String()
    age = datatypes.Integer()
    gender = datatypes.Function('validate_gender')

    def validate_gender(self, val, **kwargs):
        val = val.lower()
        if val == 'male' or val == 'female':
            return True
        return False

validator = PersonValidator()

payload1 = {
    'name': 'Vaidik Kapoor',
    'age': 16.5,
    'gender': 'mail'
}
validator.validate(payload1)

payload2 = {
    'name': 'Vaidik Kapoor',
    'age': 16,
    'gender': 'male'
}
validator.validate(payload2)