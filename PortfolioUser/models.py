from django.db import models
from django.contrib.auth.models import User, UserManager


class PortfolioUser(User):
    nickname = models.CharField(max_length=100, null=True, blank=True)
    statement = models.TextField()
    last_activity = models.DateTimeField(auto_now_add=True, blank=True)
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()