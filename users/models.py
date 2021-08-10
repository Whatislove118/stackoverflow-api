from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    login = models.CharField(max_length=150, blank=True, unique=False)

