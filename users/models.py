from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=150)