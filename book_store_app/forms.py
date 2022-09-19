from book_store_app.models import ProfileDataModel
from django import forms
from django.forms import ModelForm


class SingUpForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='password', max_length=50, widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=50, widget=forms.PasswordInput)


class ProfileForm(ModelForm):
    first_name = forms.CharField(label='First name', max_length=100, required=False)
    last_name = forms.CharField(label='Last name', max_length=100, required=False)

    class Meta:
        model = ProfileDataModel
        fields = ['country', 'city', 'address', 'zip_or_postal_code', 'phone']


