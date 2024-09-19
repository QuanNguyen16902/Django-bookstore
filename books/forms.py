
from django import forms

class LoginForm(forms.Form):
        email = forms.EmailField(
            label='Email address',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            })
        )
        password = forms.CharField(
            label='Password',
            widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password'
            })
        )
