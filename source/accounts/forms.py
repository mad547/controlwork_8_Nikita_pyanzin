from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    avatar = forms.ImageField(
        required=True,
        label='Аватар',
    )
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'})
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'avatar', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
        }