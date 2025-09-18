from django.db import models
from django.contrib.auth.models import AbstractUser


# Minimal custom user model used by the project. Keep this stable once migrations
# are created: changing `AUTH_USER_MODEL` after initial migrations is disruptive.
class User(AbstractUser):
	email = models.EmailField('email address', unique=True)
	is_election_admin = models.BooleanField(default=False)

	def __str__(self):
		return self.username
