import re
from django.utils.deconstruct import deconstructible
from django.core.validators import ValidationError
from functools import reduce


@deconstructible
class ValidThruValidator:
    code = 'invalid format'
    valid_thru_regex = r'^(0[1-9]|1[0-2])\/[0-9]{2}$'

    def __call__(self, value):
        if not re.match(self.valid_thru_regex, value):
            raise ValidationError('Incorrect VALID THRU')
        return True


@deconstructible
class CardOwnerValidator:
    code = 'invalid format'

    def __call__(self, value):
        if not str(value).isupper():
            raise ValidationError('Incorrect format')


@deconstructible
class CardNumberValidator:
    code = 'invalid number'

    def __call__(self, value):
        if not self.luhn_validation(value):
            raise ValidationError('Incorrect card number')

    def luhn_validation(self, value):
        # Предварительно рассчитанные результаты умножения на 2 с вычетом 9 для больших цифр
        # Номер индекса равен числу, над которым проводится операция
        LOOKUP = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
        code = reduce(str.__add__, filter(str.isdigit, value))
        evens = sum(int(i) for i in code[-1::-2])
        odds = sum(LOOKUP[int(i)] for i in code[-2::-2])
        return ((evens + odds) % 10 == 0)


validate_valid_thru = ValidThruValidator()
validate_card_owner = CardOwnerValidator()
validate_card_number = CardNumberValidator()
