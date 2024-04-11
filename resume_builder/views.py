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


from django.shortcuts import render, redirect
from .models import Resume, ResumeDetails
import pytesseract
from pdf2image import convert_from_path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

def upload_resume(request):
    if request.method == 'POST':
        resume = request.FILES['resume']
        Resume.objects.create(resume_file=resume)
        return redirect("extract_text")
    return render(request, 'upload.html')

from django.http import JsonResponse

def extract_text(request):
    if request.method == 'POST':
        # Get the latest uploaded resume
        resume = Resume.objects.last()  
        resume_path = resume.resume_file.path

        # Convert PDF to image
        images = convert_from_path(resume_path)

        extracted_text = ""
        for img in images:
            extracted_text += pytesseract.image_to_string(img)

        # Perform sentiment analysis on the extracted text using VADER
        analyzer = SentimentIntensityAnalyzer()
        sentiment = analyzer.polarity_scores(extracted_text)

        # Split the extracted text into separate lines
        split_text = extracted_text.split('\n')

        # Organize the data into separate categories
        data = {
            'sentiment': sentiment,
            'certifications': [],
            'skills': [],
            'experience': [],
            'education': [],
            'contact': [],
            'summary': [],
            'about': [],
            'achievements': [],
            'languages': [],
            'projects': [],
            'internship': [],
        }

        current_category = None
        for line in split_text:
            line = line.strip()
            if line.upper() in ['CERTIFICATIONS', 'SKILLS', 'EDUCATION', 'CONTACT', 'SUMMARY', 'ABOUT', 'ACHIEVEMENTS',
                                'LANGUAGES', 'PROJECTS', 'INTERNSHIP']:
                current_category = line.upper()
            elif line.upper().startswith('EXPERIENCE') or line.upper().startswith('PROFESSIONAL EXPERIENCE'):
                current_category = 'EXPERIENCE'
            elif line.upper().startswith('SUMMARY') or line.upper().startswith('PROFILE SUMMARY'):
                current_category = 'SUMMARY'
            elif line.upper().startswith('LANGUAGES') or line.upper().startswith('LANGUAGES KNOWN'):
                current_category = 'LANGUAGES'
            elif line.upper().startswith('SKILLS') or line.upper().startswith('KEY SKILLS'):
                current_category = 'SKILLS'

            elif current_category:
                # Remove special characters from the line using regular expressions
                line = re.sub(r'[^\w\s]', '', line)
                # Ensure that the line is not empty after removing special characters
                if line:
                    data[current_category.lower()].append(line)

        # Join summary, projects, and education lists into single strings
        data['summary'] = '\n'.join(data['summary'])
        data['projects'] = '\n'.join(data['projects'])
        data['education'] = '\n'.join(data['education'])

        # Create a ResumeDetails object with the extracted data
        ResumeDetails.objects.create(
            summary=data['summary'],
            skills=', '.join(data['skills']),
            projects=data['projects'],
            languages=', '.join(data['languages']),
            education=data['education'],
            internship=data['internship'],
            experience=data['experience'],
            contact=data['contact'],
            certifications=data['certifications']
        )

        # You can return a JSON response if needed
        return JsonResponse(data)

    # Return a default response if not a POST request
    return JsonResponse({'message': 'Invalid request method'})
