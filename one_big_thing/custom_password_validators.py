import string

from django.core.exceptions import ValidationError


class SpecialCharacterValidator:
    msg = "The password must contain at least one special character."

    def validate(self, password, user=None):
        special_characters = string.punctuation
        msg = "The password must contain at least one special character."

        if not any(char in special_characters for char in password):
            raise ValidationError(self.msg)

    def get_help_text(self):
        return self.msg


class LowercaseUppercaseValidator:
    msg = "The password must contain at least one lowercase character and one uppercase character."

    def validate(self, password, user=None):
        contains_lowercase = any(char.islower() for char in password)
        contains_uppercase = any(char.isupper() for char in password)

        if (not contains_lowercase) or (not contains_uppercase):
            raise ValidationError(self.msg)

    def get_help_text(self):
        return self.msg
