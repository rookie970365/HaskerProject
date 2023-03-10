from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)


class LogInForm(AuthenticationForm):
    pass


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")


class ChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "photo")
