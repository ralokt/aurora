from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from AuroraUser.models import AuroraUser

"""
Custom authentication backend to just pass the AuroraUser
instead of the default Django user in request context.
"""

class AuroraAuthenticationBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = AuroraUser
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = AuroraUser.objects.get(matriculation_number=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return ModelBackend.authenticate(self, username=username, password=password, **kwargs)

    def get_user(self, user_id):
        try:
            return AuroraUser._default_manager.get(pk=user_id)
        except User.DoesNotExist:
            return None