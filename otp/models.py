from django.db import models

# Create your models here.
class OTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.email}"