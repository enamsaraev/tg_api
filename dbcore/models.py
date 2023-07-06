from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.conf import settings


class User(AbstractBaseUser):
    """Custon user model that supportsusing email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    chat_id = models.BigIntegerField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)

    first_name = None
    last_name = None
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

