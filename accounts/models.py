from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=False)
    native = models.CharField(max_length=100, blank=False)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        blank=False
    )
    type = models.CharField(
        max_length=20,
        choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Expert', 'Expert')],
        null=True,  # ✅ Allows null initially
        blank=True  # ✅ Allows blank entry
    )

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def __str__(self):
        return self.username


