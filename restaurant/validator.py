from rest_framework.exceptions import ValidationError


def validate_score(value):
    if value < 0 or value > 10:
        raise ValidationError(f"You must set score from 0 to 10, you set {value}")


def validate_price(value):
    if value < 0:
        raise ValidationError(f"Price can't be lower than 0, you set {value}")
