
from django import forms

from django.contrib.auth.forms import UserCreationForm

from  .models import MyUser









class MyUserForm(forms.Form):

    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码')
    class Meta:

        model = MyUser

        fields = ['username','password']
