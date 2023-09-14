from django.core.exceptions import ValidationError
from nose.tools import assert_raises_regexp

from one_big_thing.custom_password_validators import (
    BusinessPhraseSimilarityValidator,
    LowercaseUppercaseValidator,
    SpecialCharacterValidator,
)


def test_special_character_validator_pass():
    """we expect `password#' to pass because it contains the special character `#`"""
    validator = SpecialCharacterValidator()
    validator.validate("password#")
    assert True


def test_special_character_validator_fail():
    """we expect `password' to fail because it contains no special characters"""
    validator = SpecialCharacterValidator()
    with assert_raises_regexp(ValidationError, validator.msg):
        validator.validate("password")


def test_lowercase_uppercase_validator_pass():
    """we expect `PassWord' to pass because it contains a mix of upper and lower case
    letters
    """
    validator = LowercaseUppercaseValidator()
    validator.validate("PassWord")
    assert True


def test_lowercase_uppercase_validator_fail():
    """we expect `password' to fail because is entirely lower case"""
    validator = LowercaseUppercaseValidator()
    with assert_raises_regexp(ValidationError, validator.msg):
        validator.validate("password")


def test_business_phrase_similarity_validator_pass():
    """we expect `password' to pass because it isnt black listed"""
    validator = BusinessPhraseSimilarityValidator()
    validator.validate("PassWord")
    assert True


def test_business_phrase_similarity_validator_fail():
    """we expect `password' to fail because 'downing-street' is a blacklisted
    password"""
    validator = BusinessPhraseSimilarityValidator()
    with assert_raises_regexp(ValidationError, validator.msg):
        validator.validate("number 10 downing-street")
