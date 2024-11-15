from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # Link this model to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add your additional fields
    email = models.EmailField(max_length=254)
    
    def __str__(self):
        return self.user.username
