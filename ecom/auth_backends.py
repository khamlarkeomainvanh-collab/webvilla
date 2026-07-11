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
    """Lets customers log in with their (auto-generated) username, the phone
    number they typed at signup, or their own name — most customers don't
    remember the generated 'u<mobile>' username and naturally try their name
    or phone number instead. Name isn't unique across customers, so every
    matching account is tried against the given password rather than trusting
    the first match."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        User = get_user_model()
        typed = username.strip()

        # 1) exact username match (the generated 'u<mobile>' string)
        user = User.objects.filter(username=typed).first()
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user

        # 2) phone number typed at signup (Customer.mobile)
        target_phone = _normalize_phone(typed)
        if target_phone:
            for cust in models.Customer.objects.exclude(mobile='').select_related('user'):
                if _normalize_phone(cust.mobile) == target_phone:
                    if cust.user.check_password(password) and self.user_can_authenticate(cust.user):
                        return cust.user

        # 3) first name / full name (not unique — check every match's password)
        name_candidates = User.objects.filter(first_name__iexact=typed)
        for u in name_candidates:
            if u.check_password(password) and self.user_can_authenticate(u):
                return u

        # 4) full name ("first last") in case they typed both
        for u in User.objects.exclude(first_name=''):
            full_name = f"{u.first_name} {u.last_name}".strip()
            if full_name.lower() == typed.lower():
                if u.check_password(password) and self.user_can_authenticate(u):
                    return u

        return None
