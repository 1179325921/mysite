import re
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20, min_length=5, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '请输入3-30位用户名'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password_again = forms.CharField(label='确认密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        have_symbol = re.match('^[a-z0-9]+$', username)
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户已存在')
        elif len(username) > 20:
            raise forms.ValidationError('用户名长度不能超过20')
        elif have_symbol:
            raise forms.ValidationError('用户名不能包含特殊字符')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被使用')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password_again != password:
            raise forms.ValidationError('两次密码输入不一致')
        return password
