from django.db import models

class Resume(models.Model):
    resume_file = models.FileField(upload_to='resumes/')


class ResumeDetails(models.Model):
    summary=models.CharField(max_length=5000, default='Add Your Summry')
    skills=models.CharField(max_length=5000, default='Add Your Skills')
    projects=models.CharField(max_length=5000, default='Add Your projects')
    languages=models.CharField(max_length=5000, default='Add Your languages')
    education=models.CharField(max_length=5000, default='Add Your education')
    internship=models.CharField(max_length=5000, default='Add Your internship')
    experience=models.CharField(max_length=5000, default='Add Your experience')
    contact=models.CharField(max_length=5000, default='Add Your contact')
    certifications=models.CharField(max_length=5000, default='Add Your certifications')