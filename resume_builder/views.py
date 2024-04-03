from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden,HttpResponseBadRequest
from django.template import loader


def user_select_theme(request):
    return render(request,'user_select_theme.html')

def temp1(request):
    return render(request,'temp1.html')


def temp2(request):
    return render(request,'temp2.html')


def temp3(request):
    return render(request,'temp3.html')