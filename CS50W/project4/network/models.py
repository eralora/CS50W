from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
	new_post = models.CharField(max_length=200, null=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	like = models.ManyToManyField(User, blank=True, related_name="liked_user")

	def __str__(self):
		return self.user.username
