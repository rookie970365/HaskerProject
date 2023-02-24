from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def size_validator(photo):
    max_size = 5
    if photo.size > max_size * 1024 * 1024:
        raise ValidationError(f"The maximum file size is {max_size}MB")
    return photo


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    photo = models.ImageField(
        blank=True,
        upload_to='avatars/%Y/%m/%d',
        validators=[size_validator],
        default="default.png",
    )

    def get_photo_url(self):
        return self.photo.url
