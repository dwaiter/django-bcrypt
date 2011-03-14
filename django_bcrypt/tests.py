import bcrypt

from django.conf import settings
from django.contrib.auth.models import User, UNUSABLE_PASSWORD
from django.test import TestCase

from django_bcrypt.models import (bcrypt_check_password, bcrypt_set_password,
                                  _check_password, _set_password, get_rounds)




class CheckPasswordTest(TestCase):
    def test_bcrypt_password(self):
        user = User()
        bcrypt_set_password(user, 'password')
        self.assertTrue(bcrypt_check_password(user, 'password'))
        self.assertFalse(bcrypt_check_password(user, 'invalid'))

    def test_sha1_password(self):
        user = User()
        _set_password(user, 'password')
        self.assertTrue(bcrypt_check_password(user, 'password'))
        self.assertFalse(bcrypt_check_password(user, 'invalid'))

    def test_change_rounds(self):
        user = User()
        orig_rounds = getattr(settings, 'BCRYPT_ROUNDS', None)
        try:
            # Hash with 5 rounds
            settings.BCRYPT_ROUNDS = 5
            bcrypt_set_password(user, 'password')
            password_5 = user.password
            self.assertTrue(bcrypt_check_password(user, 'password'))
            # Hash with 12 rounds
            settings.BCRYPT_ROUNDS = 12
            bcrypt_set_password(user, 'password')
            password_12 = user.password
            self.assertTrue(bcrypt_check_password(user, 'password'))
        finally:
            if hasattr(settings._wrapped, 'BCRYPT_ROUNDS'):
                delattr(settings._wrapped, 'BCRYPT_ROUNDS')


class SetPasswordTest(TestCase):
    def assertBcrypt(self, hashed, password):
        self.assertEqual(hashed[:3], 'bc$')
        self.assertEqual(hashed[3:], bcrypt.hashpw(password, hashed[3:]))

    def test_set_password(self):
        user = User()
        bcrypt_set_password(user, 'password')
        self.assertBcrypt(user.password, 'password')

    def test_set_unusable_password(self):
        user = User()
        bcrypt_set_password(user, None)
        self.assertEqual(user.password, UNUSABLE_PASSWORD)

    def test_change_rounds(self):
        user = User()
        orig_rounds = getattr(settings, 'BCRYPT_ROUNDS', None)
        try:
            # No rounds should still produce a salted password
            settings.BCRYPT_ROUNDS = 0
            bcrypt_set_password(user, 'password')
            self.assertBcrypt(user.password, 'password')
        finally:
            if hasattr(settings._wrapped, 'BCRYPT_ROUNDS'):
                delattr(settings._wrapped, 'BCRYPT_ROUNDS')


class SettingsTest(TestCase):
    def test_get_rounds(self):
        orig_rounds = getattr(settings, 'BCRYPT_ROUNDS', None)
        try:
            settings.BCRYPT_ROUNDS = 0
            self.assertEqual(get_rounds(), 0)
            settings.BCRYPT_ROUNDS = 5
            self.assertEqual(get_rounds(), 5)
            delattr(settings, 'BCRYPT_ROUNDS')
            self.assertEqual(get_rounds(), 12)
        finally:
            if hasattr(settings._wrapped, 'BCRYPT_ROUNDS'):
                delattr(settings._wrapped, 'BCRYPT_ROUNDS')
