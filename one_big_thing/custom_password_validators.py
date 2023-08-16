import re
import string
from difflib import SequenceMatcher

from django.core.exceptions import ValidationError

# TODO - could add more to list
BUSINESS_SPECIFIC_WORDS = [
    "one big thing",
    "whitehall",
    "civil service",
    "home office",
    "cabinet office",
    "10 downing street",
]


class SpecialCharacterValidator:
    msg = "The password must contain at least one special character."

    def validate(self, password, user=None):
        special_characters = string.punctuation

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


# Replicates functionality of UserAttributeSimilarityValidator, but don't need a user
def similarity_password_validator(password, comparator_string, max_similarity=0.7):
    substrings = re.split(r"\W+", comparator_string) + [comparator_string]
    for part in substrings:
        similarity = SequenceMatcher(a=password.lower(), b=part.lower()).quick_ratio()
        if similarity >= max_similarity:
            raise ValidationError("The password is too similar to the email.")


class BusinessPhraseSimilarityValidator:
    msg = "The password should not contain business specific words."

    def validate(self, password, user=None):
        password_lower = password.lower()
        for phrase in BUSINESS_SPECIFIC_WORDS:
            if phrase.replace(" ", "") in password_lower:
                raise ValidationError(self.msg)
            elif phrase.replace(" ", "_") in password_lower:
                raise ValidationError(self.msg)
            elif phrase.replace(" ", "-") in password_lower:
                raise ValidationError(self.msg)
