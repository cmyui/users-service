from app.validators import accounts
import pytest


@pytest.mark.parametrize(
    ("phone_number", "expected"),
    (
        ("+1 415 555 2671", True),
        ("+1 415-555-2671", True),
        ("+1 415.555.2671", True),
        ("1 415 555 2671", False),
        ("415 555 2671", False),
        ("4155552671", False),
        ("1 415-555-2671", False),
        ("415-555-2671", False),
        ("1 415.555.2671", False),
        ("415.555.2671", False),
        ("+1 415 555 2671 ext. 1234", True),
        ("+1 415 555 2671 #1234", True),
    ),
)
def test_validate_phone_number(phone_number: str, expected: bool):
    result = accounts.validate_phone_number(phone_number)
    assert result == expected


@pytest.mark.parametrize(
    ("email_address", "expected"),
    (
        ("john.doe@example.com", True),
        ("jane_doe@example.co.uk", True),
        ("my.email+123@gmail.com", True),
        ("firstname.lastname@company.io", True),
        ("john-doe_123@domain.com", True),
        ("john.doe@example", False),  # (missing the top-level domain)
        ("john.doe@.com", False),  # (missing the domain name)
        ("john.doe@example..com", False),  # (double dot before the top-level domain)
        ("john.doe@example@.com", False),  # (double @ symbol)
        ("john.doe@%&/", False),  # (invalid domain name with special characters)
    ),
)
def test_validate_email_address(email_address: str, expected: bool):
    result = accounts.validate_email_address(email_address)
    assert result == expected


@pytest.mark.parametrize(
    ("password", "expected"),
    (
        ("Abcdef12", True),
        ("A1b2C3d4", True),
        ("P@ssW0rd", True),
        ("L0nG3rP@ssw0rd", True),
        ("S3cur3P@55", True),
        ("abcdef12", False),  # (missing an uppercase letter)
        ("Abcdefgh", False),  # (missing a digit)
        ("ABCDEF12", False),  # (missing a lowercase letter)
        ("Abcdef1", False),  # (too short - only 7 characters)
        ("password", False),  # (missing an uppercase letter and a digit)
        ("PASSWORD", False),  # (missing a lowercase letter and a digit)
        ("12345678", False),  # (missing an uppercase and lowercase letter)
    ),
)
def test_validate_password(password: str, expected: bool):
    result = accounts.validate_password(password)
    assert result == expected
