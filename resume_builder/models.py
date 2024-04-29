from django.db import models
from django.contrib.auth.models import AbstractUser


class NewUser(AbstractUser):
    phone_no = models.CharField(max_length=100, default='contact no')
    linkedin = models.CharField(max_length=400,default="linkedin url")


class Resume(models.Model):
    resume_file = models.FileField(upload_to='resumes/')


class ResumeDetails(models.Model):
    user_id=models.ForeignKey('NewUser', on_delete=models.CASCADE)
    summary=models.CharField(max_length=5000, default='Add Your Summry')
    skills=models.CharField(max_length=5000, default='Add Your Skills')
    projects=models.CharField(max_length=5000, default='Add Your projects')
    languages=models.CharField(max_length=5000, default='Add Your languages')
    education=models.CharField(max_length=5000, default='Add Your education')
    internship=models.CharField(max_length=5000, default='Add Your internship')
    experience=models.CharField(max_length=5000, default='Add Your experience')
    contact=models.CharField(max_length=5000, default='Add Your contact')
    certifications=models.CharField(max_length=5000, default='Add Your certifications')

class ExperienceDetails(models.Model):
    user_id=models.ForeignKey('NewUser', on_delete=models.CASCADE)
    company_name=models.CharField(max_length=5000, default='Add Your university')
    designation=models.CharField(max_length=5000, default='Add Your Designation')
    start_date=models.CharField(max_length=5000, default='Add Your Start date')
    end_date=models.CharField(max_length=5000, default='Add Your end date')


class EducationDetails(models.Model):
    user_id=models.ForeignKey('NewUser', on_delete=models.CASCADE)
    degree=models.CharField(max_length=5000, default='Add Your Degree')
    university=models.CharField(max_length=5000, default='Add Your university')
    
    year_of_passing=models.CharField(max_length=5000, default='Add Your year of passing')