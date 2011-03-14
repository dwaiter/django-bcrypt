import bcrypt

from django.contrib.auth.models import User, UNUSABLE_PASSWORD
from django.test import TestCase

from django_bcrypt.models import (bcrypt_check_password, bcrypt_set_password,
                                  _check_password)


class CheckPasswordTest(TestCase):
    def test_bcrypt_password(self):
        user = User()
        bcrypt_set_password(user, 'password')
        self.assertTrue(bcrypt_check_password(user, 'password'))
        self.assertFalse(bcrypt_check_password(user, 'invalid'))


class SetPasswordTest(TestCase):
    def test_set_password(self):
        user = User()
        bcrypt_set_password(user, 'password')
        self.assertEqual(user.password[:3], 'bc$')
        self.assertEqual(user.password[3:],
                         bcrypt.hashpw('password', user.password[3:]))

    def test_set_unusable_password(self):
        user = User()
        bcrypt_set_password(user, None)
        self.assertEqual(user.password, UNUSABLE_PASSWORD)
