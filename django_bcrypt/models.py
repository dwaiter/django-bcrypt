"""
Overrides :class:`django.contrib.auth.models.User` to use bcrypt
hashing for passwords.

You can set the following ``settings``:

``BCRYPT_ENABLED``
   Enables bcrypt hashing when ``User.set_password()`` is called.

``BCRYPT_ENABLED_UNDER_TEST``
   Enables bcrypt hashing when running inside Django
   TestCases. Defaults to False, to speed up user creation.

``BCRYPT_ROUNDS``
   Number of rounds to use for bcrypt hashing. Defaults to 12.
"""


import bcrypt

from django.contrib.auth.models import User
from django.conf import settings
from django.core import mail


def get_rounds():
    """Returns the number of rounds to use for bcrypt hashing."""
    return getattr(settings, "BCRYPT_ROUNDS", 12)


def is_enabled():
    """Returns ``True`` if bcrypt should be used."""
    enabled = getattr(settings, "BCRYPT_ENABLED", True)
    if not enabled:
        return False
    # Are we under a test?
    if hasattr(mail, 'outbox'):
        return getattr(settings, "BCRYPT_ENABLED_UNDER_TEST", False)
    return True


def migrate_to_bcrypt():
    """Returns ``True`` if password migration is activated. """
    migrated = getattr(settings, "BCRYPT_MIGRATE", False)
    if not migrated:
        return False
    return True


def bcrypt_check_password(self, raw_password):
    """
    Returns a boolean of whether the *raw_password* was correct.

    If bcrypt migration is activated, validate password only
    with bcrypt. If not, attempt to validate with bcrypt, but fall back
    to Django's ``User.check_password()`` if the hash is incorrect.
    """
    if migrate_to_bcrypt:
        if self.password.startswith('sha1$')
            and _check_password(self, raw_password):
            bcrypt_set_password(self, raw_password)
            return bcrypt.hashpw(raw_password, salt_and_hash) == salt_and_hash
        elif self.password.startswith('bc$'):
            salt_and_hash = self.password[3:]
            return bcrypt.hashpw(raw_password, salt_and_hash) == salt_and_hash
        return _check_password(self, raw_password)
    else:
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
    if not is_enabled() or raw_password is None:
        _set_password(self, raw_password)
    else:
        salt = bcrypt.gensalt(get_rounds())
        self.password = 'bc$' + bcrypt.hashpw(raw_password, salt)
_set_password = User.set_password
User.set_password = bcrypt_set_password
