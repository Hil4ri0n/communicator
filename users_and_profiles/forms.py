from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Profile, FriendRequest
from django import forms


class UserRegisterForm(UserCreationForm):

    nickname = forms.CharField(max_length=30)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if Profile.objects.filter(nickname=nickname).exists():
            raise ValidationError("This nickname is already taken. Please choose a different one.")
        return nickname


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'nickname']





