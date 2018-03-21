from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from custom_user.models import User, PasswordReset
from django.contrib.auth import authenticate, login, logout
import uuid
from django.contrib import messages

"""
CREATE NEW DESINGER ACCOUNT
"""
def create_designer_account(request):
    # prepare error flag
    error = ""
    form_name = ""
    form_email = ""
    if request.method == 'POST':
        print(" it is post")
        user_name = request.POST.get('username',None)
        user_email = request.POST.get('email',None)
        user_password1 = request.POST.get('password1',None)
        user_password2 = request.POST.get('password2',None)

        # just save information
        form_name = user_name
        form_email = user_email

        # check password
        if user_password1 == user_password2:
            # create usre
            try:
                user = User.objects.create_user(username=user_name,
                                                email=user_email,
                                                password=user_password1,
                                                account='designer')
                user.is_active = True
                user.save()
                return HttpResponseRedirect(reverse('dashboard_top'))
            except Exception as e:
                error = "無効なメールアドレスです"
        else:
            error = "パスワードが一致しません"
    context = {
        'bg_color':'bg-gray',
        'form_username':form_name,
        'form_email':form_email,
        'error':error
    }
    return render(request,'auth/create_designer_account.html',context)

"""
LOGIN
"""
def login_account(request):
    # prepare error flag
    error = ""

    if request.method == 'POST':
        user_email = request.POST.get('email',None)
        user_password = request.POST.get('password',None)
        print(user_email)
        print(user_password)
        # try to login
        user = authenticate(email=user_email, password=user_password)
        if user is not None:

            login(request, user)
            # change redirect page by account
            if user.account == 'designer':
                return HttpResponseRedirect(reverse('dashboard_top'))
            else:
                # reset password when client is suspend
                if user.is_suspend == True:
                    try:
                        reset_password = PasswordReset.objects.get(email=user.email)
                        logout(request)
                        messages.success(request,'初回ログインのためパスワードを再設定してください')
                        return HttpResponseRedirect(reverse('reset_password',kwargs={'key':reset_password.access_key}))
                    except PasswordReset.DoesNotExist:
                        logout(request)
                        pass
                else:
                    return HttpResponseRedirect(reverse('dashboard_top'))
        else:
            error = "ログイン情報をお確かめください"
    context = {
        'bg_color':'bg-gray',
        'error':error
    }
    return render(request,'auth/login_account.html',context)

"""
LOGOUT
"""
def logout_account(request):
    logout(request)
    messages.success(request,'ログアウトしました')
    return HttpResponseRedirect(reverse('login_account'))

"""
RESET PASSWORD REQUEST
"""
def reset_password_request(request):
    error = ""
    success = ""
    if request.method == 'POST':
        user_email = request.POST.get('email',None)
        users = User.objects.filter(email=user_email)

        if len(users) == 0:
            error = "該当するユーザーが存在しません"
        else:

            # make sure that instance is exist or not
            reset_instance = PasswordReset.objects.filter(email=user_email)

            if len(reset_instance) == 0:
                uuid_key = str(uuid.uuid4())
                reset_password = PasswordReset(email=user_email,access_key=uuid_key)
                reset_password.save()
                success = "再設定用のメールを送信しました"
            else:
                error = "すでに再設定用のメールをお送りしています"
    context = {
        'bg_color':'bg-gray',
        'error':error,
        'success':success
    }
    return render(request,'auth/reset_password_request.html',context)

"""
RESET PASSWORD
"""
def reset_password(request,key):
    error = ""
    form_email = ""
    # try to find object
    try:
        password_reset = PasswordReset.objects.get(access_key=key)

        # reset password
        if request.method == 'POST':
            reset_email = request.POST.get('email',None)
            password1   = request.POST.get('password1',None)
            password2   = request.POST.get('password2',None)

            if password_reset.email == reset_email:
                if password1 == password2:
                    user = User.objects.get(email=reset_email)
                    user.set_password(password1)
                    user.is_suspend = False
                    user.save()

                    # delete password_reset object
                    password_reset.delete()
                    messages.success(request,'パスワードの再設定が完了しました')
                    return HttpResponseRedirect(reverse('login_account'))
                else:
                    form_email = reset_email
                    error = "パスワードが一致しません"
            else:
                form_email = ""
                error = "メールアドレスが無効です"
    except PasswordReset.DoesNotExist:
        error = "無効なキーです"
    context = {
        'bg_color':'bg-gray',
        'error':error,
        'ac_key':key,
        'form_email':form_email
    }

    return render(request,'auth/reset_password.html',context)
