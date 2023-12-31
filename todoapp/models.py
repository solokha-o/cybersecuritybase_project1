from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User model with insecure password management, as plaintext passwords are stored in database."""

    # Suggested fix for flaw would be to simply remove this overrided method to enable Django's built-in way for password management
    def enter_password(self, raw_password):
        self.password = raw_password
        self._password = raw_password

    # Also, this method should be removed to fix security flaw
    def validate_password(self, entered_password):
        return entered_password == self.password

    class Meta:
        db_table = "auth_user"


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField()
    done = models.BooleanField(default=False)
