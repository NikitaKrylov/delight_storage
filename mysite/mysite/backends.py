from django.contrib.auth.backends import BaseBackend
from accounts.models import User
from django.db.models import Q


class AuthBackend(BaseBackend):

    supports_object_permissions = True
    supports_anonymouse_user = False
    supports_inactive_user = False

    def authenticate(self, request, username=None, password=None):
        try:
            user: User = User.objects.get(
                Q(username=username) | Q(email=username)
            )
        except User.DoesNotExist:
            return None

        return user if user.check_password(password) else None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
