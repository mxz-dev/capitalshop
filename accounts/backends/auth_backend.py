from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from accounts.models import CustomUser


class AuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        UserModel = CustomUser
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
    def get_user(self, user_id):
        UserModel = CustomUser
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None