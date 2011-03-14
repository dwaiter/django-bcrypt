"""
Overrides :class:`django.contrib.auth.models.User` to use bcrypt
hashing for passwords.
"""


import bcrypt

from django.contrib.auth.models import User
from django.conf import settings


def get_rounds():
    """
    Returns the number of rounds to use for bcrypt hashing.

    Retrieves this from :data:`settings.BCRYPT_ROUNDS`.
    """
    return getattr(settings, "BCRYPT_ROUNDS", 12)


def bcrypt_check_password(self, raw_password):
    """
    Returns a boolean of whether the *raw_password* was correct.

    Attempts to validate with bcrypt, but falls back to Django's
    ``User.check_password()`` if the hash is incorrect.
    """
    if self.password.startswith('bc$'):
        salt_and_hash = self.password[3:]
        return bcrypt.hashpw(raw_password, salt_and_hash) == salt_and_hash
    return _check_password(self, raw_password)
_check_password = User.check_password
User.check_password = bcrypt_check_password


def bcrypt_set_password(self, raw_password):
    """
    Sets the user's password to *raw_password*, hashed with bcrypt.
    """
    if raw_password is None:
        self.set_unusable_password()
    else:
        salt = bcrypt.gensalt(get_rounds())
        self.password = 'bc$' + bcrypt.hashpw(raw_password, salt)
_set_password = User.set_password
User.set_password = bcrypt_set_password
