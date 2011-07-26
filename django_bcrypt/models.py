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

``BCRYPT_MIGRATE``
   Enables bcrypt password migration on a check_password() call.
   Default is set to False.
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
    """Returns ``True`` if password migration is activated."""
    return getattr(settings, "BCRYPT_MIGRATE", False)


def bcrypt_check_password(self, raw_password):
    """
    Returns a boolean of whether the *raw_password* was correct.

    Attempts to validate with bcrypt, but falls back to Django's
    ``User.check_password()`` if the hash is incorrect.

    If ``BCRYPT_MIGRATE`` is set, attempts to convert sha1 password to bcrypt
    or converts between different bcrypt cost values.

    .. note::

        In case of a password migration this method calls ``User.save()`` to
        persist the changes.
    """
    result = False
    if self.password.startswith('bc$'):
        salt_and_hash = self.password[3:]
        result = bcrypt.hashpw(raw_password, salt_and_hash) == salt_and_hash
    elif _check_password(self, raw_password):
        result = True
        if is_enabled() and migrate_to_bcrypt():
            self.set_password(raw_password)
            salt_and_hash = self.password[3:]
            assert bcrypt.hashpw(raw_password, salt_and_hash) == salt_and_hash
            self.save()
    return result
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
