import bcrypt
from django.contrib.auth.models import User
from django.conf import settings


rounds = getattr(settings, "BCRYPT_ROUNDS", 12)
_check_password = User.check_password

def bcrypt_check_password(self, raw_password):
    if self.password.startswith('bc$'):
        salt_and_hash = self.password[3:]
        return bcrypt.hashpw(raw_password, salt_and_hash) == salt_and_hash
    return _check_password(self, raw_password)

def bcrypt_set_password(self, raw_password):
    if raw_password is None:
        self.set_unusable_password()
    else:
        salt = bcrypt.gensalt(rounds)
        self.password = 'bc$' + bcrypt.hashpw(raw_password, salt)

User.check_password = bcrypt_check_password
User.set_password = bcrypt_set_password

