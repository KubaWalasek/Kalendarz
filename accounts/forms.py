from django.contrib.auth import get_user_model
from django import forms as dj_forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django import forms

from accounts.models import Adres

User = get_user_model()


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email']


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class UpdatePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class AdresForm(forms.ModelForm):
    class Meta:
        model = Adres
        fields = ['post_code', 'city', 'street', 'house_number', 'apartment_number', 'phone_number']


class DeleteUserForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        pwd = self.cleaned_data['password']
        if not self.user or not self.user.check_password(pwd):
            raise forms.ValidationError('Nieprawidłowe hasło.')
        return pwd





