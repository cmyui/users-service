import email_validator
import phonenumbers


def validate_username(username: str) -> bool:
    if len(username) < 4:
        return False
    if not username.isalnum():
        return False
    return True

def validate_phone_number(phone_number: str) -> bool:
    try:
        phonenumbers.parse(phone_number)
    except phonenumbers.NumberParseException:
        return False
    else:
        return True


def validate_email_address(email_address: str) -> bool:
    try:
        email_validator.validate_email(email_address)
    except email_validator.EmailNotValidError:
        return False
    else:
        return True


def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True
