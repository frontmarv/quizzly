from django.db import models


class User(models.Model):
    """Represents a user account.

    Attributes:
        email: Unique email address for the user
        username: Unique username for the user
    """
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
