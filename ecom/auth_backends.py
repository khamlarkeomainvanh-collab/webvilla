import re
import unicodedata

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from . import models


def _normalize_phone(raw):
    digits = re.sub(r'\D', '', raw or '')
    if digits.startswith('856'):
        digits = digits[3:]
    return digits.lstrip('0')


def _norm_name(raw):
    """NFKC-normalize + casefold so name comparisons survive Django's login
    form silently NFKC-normalizing the submitted username (it does this on
    every text login field, to guard against unicode look-alike spoofing).
    For Lao script that normalization rewrites some very common letters —
    e.g. 'ຳ' (U+0EB3) becomes 'ໍາ' (U+0ECD U+0EB2) — so a name typed
    identically at signup and login can otherwise fail to match even though
    it looks character-for-character the same on screen."""
    return unicodedata.normalize('NFKC', (raw or '').strip()).casefold()


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

        # 3) first name, or full name ("first last") — compared after the same
        # NFKC+casefold normalization on both sides so it's immune to whatever
        # unicode form either the login form or the stored value happens to be in.
        target_name = _norm_name(typed)
        if target_name:
            for u in User.objects.exclude(first_name=''):
                full_name = f"{u.first_name} {u.last_name}".strip()
                if _norm_name(u.first_name) == target_name or _norm_name(full_name) == target_name:
                    if u.check_password(password) and self.user_can_authenticate(u):
                        return u

        return None
