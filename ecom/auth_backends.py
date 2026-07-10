import re

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from . import models


def _normalize_phone(raw):
    digits = re.sub(r'\D', '', raw or '')
    if digits.startswith('856'):
        digits = digits[3:]
    return digits.lstrip('0')


class MobileOrUsernameBackend(ModelBackend):
    """Lets customers log in with either their (auto-generated) username or
    the phone number they typed at signup — most customers only remember
    the phone number they gave, not the generated 'u<mobile>' username."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        User = get_user_model()
        user = User.objects.filter(username=username).first()
        if user is None:
            target = _normalize_phone(username)
            if target:
                for cust in models.Customer.objects.exclude(mobile='').select_related('user'):
                    if _normalize_phone(cust.mobile) == target:
                        user = cust.user
                        break
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
