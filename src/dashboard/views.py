from django.shortcuts import render, render_to_response
from django.template import RequestContext
from custom_user.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Dashboard top
@login_required(login_url='/auth/login/')
def top(request):
    context = {
        'test':'ok google'
    }
    return render(request,'dashboard/top.html',context)
