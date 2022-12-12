
import re
from rest_framework.exceptions import ValidationError


def validate_aamarpay_email(email):
    """
    Validate if email is an STIL email.
    """
    email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@aamarpay.com')
    if re.fullmatch(email_regex, email):
        return email
    raise ValidationError("Please Provide a valid STIL email.")



