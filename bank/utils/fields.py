from django.db import models

from . import validators


class CardNumberField(models.CharField):
    description = 'Card number'
    default_validators = [validators.validate_card_number]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ValidThruField(models.CharField):
    description = "Valid Thru"
    default_validators = [validators.validate_valid_thru]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CardOwnerField(models.CharField):
    description = "Card owner"
    default_validators = [validators.validate_card_owner]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
