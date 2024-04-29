from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('login',views.login_view,name='login'),
    path('user_select_theme',views.user_select_theme,name='user_select_theme'),
    path('temp1',views.temp1,name='temp1'),
    path('temp3',views.temp3,name='temp3'),
    path('temp2',views.temp2,name='temp2'),
    path('temp4',views.temp4,name='temp4'),
    path('temp5',views.temp5,name='temp5'),
    path('temp6',views.temp6,name='temp6'),
    path('temp7',views.temp7,name='temp7'),
    path('temp8',views.temp8,name='temp8'),
    path('temp9',views.temp9,name='temp9'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('get_degree_info/', views.get_degree_info, name='get_degree_info'),
    path('get_first_name_info/', views.get_first_name_info, name='get_first_name_info'),
    path('get_last_name_info/', views.get_last_name_info, name='get_last_name_info'),
   # path('get_first_name_info/', views.get_first_name_info, name='get_first_name_info'),
    path('get_designation_info/', views.get_designation_info, name='get_designation_info'),
    path('get_university_info/', views.get_university_info, name='get_university_info'),
    path('get_summary_info/', views.get_summary_info, name='get_summary_info'),
    path('get_skills_info/', views.get_skills_info, name='get_skills_info'),
    path('get_email_info/', views.get_email_info, name='get_email_info'),
    path('get_linkedin_info/', views.get_linkedin_info, name='get_linkedin_info'),
    path('get_phone_no_info/', views.get_phone_no_info, name='get_phone_no_info'),
    path('get_company_info/', views.get_company_info, name='get_company_info'),
    path('get_project_info/', views.get_project_info, name='get_project_info'),
    path('get_languages_info/', views.get_languages_info, name='get_languages_info'),

]