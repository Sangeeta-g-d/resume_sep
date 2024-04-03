from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
    path('user_select_theme',views.user_select_theme,name='user_select_theme'),
    path('temp1',views.temp1,name='temp1'),
    path('temp3',views.temp3,name='temp3'),
    path('temp2',views.temp2,name='temp2'),
]