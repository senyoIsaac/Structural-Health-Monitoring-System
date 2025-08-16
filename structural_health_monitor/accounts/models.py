from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_engineer = models.BooleanField(default=True)
    is_manager = models.BooleanField(default = False)
