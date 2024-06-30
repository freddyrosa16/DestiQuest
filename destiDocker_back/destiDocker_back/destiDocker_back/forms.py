from django import forms
from django.contrib.auth.forms import UserCreationForm
from destiDocker_back.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text="Please use a valid email address.",
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')
