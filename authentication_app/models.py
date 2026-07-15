from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Represents a user account.

    Extends Django's AbstractUser with custom configurations.
    Inherits: username, password, email, first_name, last_name, etc.
    """
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
