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



from django.shortcuts import render
from django.http import HttpResponse
from .models import Resume
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

def upload_resume(request):
    if request.method == 'POST':
        resume = request.FILES['resume']
        Resume.objects.create(resume_file=resume)
        return HttpResponse("Resume uploaded successfully!")
    return render(request, 'upload.html')

def extract_text(request):
    resume = Resume.objects.last()  # Get the latest uploaded resume
    resume_path = resume.resume_file.path

    # Convert PDF to image
    images = convert_from_path(resume_path)

    extracted_text = ""
    for img in images:
        extracted_text += pytesseract.image_to_string(img)

    return render(request, 'resume.html', {'extracted_text': extracted_text})
