from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class UploadForm(forms.Form):
    name = forms.CharField(max_length=50,help_text="Enter the name of the video")
    url = forms.CharField(max_length=1000,help_text="Enter the URL of the video")
    user = forms.CharField(max_length='5',help_text="a")
    class Meta:
        fields = ('name','url','user')