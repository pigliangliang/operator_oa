from django.shortcuts import render,reverse,redirect

# Create your views here.
from django.views.generic import View

from .forms import MyUserForm

from django.http import HttpResponse

from django.contrib.auth import authenticate,login,logout
from .models import MyUser
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password






class LoginView(View):
    def get(self,request):
        uf = MyUserForm()
        return render(request,'login.html',locals())


    def post(self,request):
        uf = MyUserForm(request.POST)
        if uf.is_valid():
            print(uf.cleaned_data)

            #这里折腾了好几个小时，使用authenticate认证是需要用的password字段是加密后的
            #否则会返回None。崩溃了。
            try:
                user = MyUser.objects.get(username=uf.cleaned_data['username'])

                if user:
                    if uf.cleaned_data['password']==user.password:

                        login(request,user)
                        return redirect(reverse('gongdan:gongdanhong'))
                    else:
                        tips = "请核对用户密码"
                        return render(request, 'login.html', locals())

            except Exception :
                tips="请核对用户信息"
                return render(request,'login.html',locals())
        else:
            tips="请核对用户信息"
            return render(request, 'login.html', locals())



class LogoutView(View):

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('users:login'))