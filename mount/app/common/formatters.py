import phonenumbers


def phone_number(phone_number: str) -> str:
    return phonenumbers.format_number(
        numobj=phonenumbers.parse(phone_number),
        num_format=phonenumbers.PhoneNumberFormat.E164,
    )
