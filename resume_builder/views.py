from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden,HttpResponseBadRequest
from django.template import loader
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from .models import NewUser
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden,HttpResponseBadRequest
from django.template import loader
import re
from django.shortcuts import render
from django.http import HttpResponse
from .models import Resume,ResumeDetails,ExperienceDetails,EducationDetails
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # Add this import
from django.http import JsonResponse


# Create your views here.
def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname= request.POST.get('Firstname')
        phone_no= request.POST.get('phone')
        lastname= request.POST.get('Lastname')
        password = request.POST.get('password')
        email = request.POST.get('email')
        contact_no = request.POST.get('phone')
        linkedin = request.POST.get('linkedin')
        passw = make_password(password)
        user = NewUser.objects.create(username=username,password=passw,
            email=email,phone_no=contact_no,first_name=firstname,last_name=lastname,
            linkedin=linkedin)
            
        return redirect('login')
    return render(request,"registration.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('user_select_theme')  # Replace 'success_url_name' with the name of your success URL
        else:
            # Return an 'invalid login' error message.
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
    
    

def user_select_theme(request):
    return render(request,'user_select_theme.html')

def extract_and_store_resume_data(resume_path, user_id):
    # Extract data from the resume
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
        'language': [],
        'declaration':[],
    }

    current_category = None
    for line in split_text:
        line = line.strip()
        if line.upper() in ['CERTIFICATIONS', 'SKILLS', 'EDUCATION', 'CONTACT', 'SUMMARY', 'ABOUT', 'ACHIEVEMENTS',
                            'LANGUAGES', 'PROJECTS', 'INTERNSHIP', 'LANGUAGE','DECLARATION']:
            current_category = line.upper()
        elif line.upper().startswith('EXPERIENCE') or line.upper().startswith('PROFESSIONAL EXPERIENCE'):
            current_category = 'EXPERIENCE'
        elif line.upper().startswith('SUMMARY') or line.upper().startswith('PROFILE SUMMARY'):
            current_category = 'SUMMARY'
        elif line.upper().startswith('ABOUT ME') or line.upper().startswith('PROFILE'):
            current_category = 'SUMMARY'
        elif line.upper().startswith('LANGUAGES') or line.upper().startswith('LANGUAGES KNOWN'):
            current_category = 'LANGUAGES'
        elif line.upper().startswith('SKILLS') or line.upper().startswith('KEY SKILLS'):
            current_category = 'SKILLS'
        elif line.upper().startswith('TECHNICAL SKILLS') or line.upper().startswith('EXPERTISE'):
            current_category = 'SKILLS'
        elif current_category:
            line = re.sub(r'[^\w\s]', '', line)
            data[current_category.lower()].append(line)

    # Join skills and summary lists into single strings
    data['summary'] = '\n'.join(data['summary'])
    first_project_line = ''
    for project_line in data['projects']:
        project_line = project_line.strip()
        if project_line:
            first_project_line = project_line
            break

    print("hhhh", first_project_line)
    data['education'] = '\n'.join(data['education'])
    data['internship'] = '\n'.join(data['internship'])
    data['experience'] = '\n'.join(data['experience'])
    data['contact'] = '\n'.join(data['contact'])
    data['certifications'] = '\n'.join(data['certifications'])
    # Filter out unwanted characters and join skills into a single string
    data['skills'] = ', '.join([skill.strip()[2:] for skill in data['skills'] if skill.strip().startswith('e ')])
    print("skills", data['skills'])

    data['languages'] = ', '.join([language.strip()[3:] for language in data['languages'] if language.strip().startswith('vy')])

    # Store the extracted data in the database
    resume_details = ResumeDetails.objects.create(
        user_id_id=user_id,
        summary=data['summary'],
        skills=data['skills'],
        projects=first_project_line,
        languages=data['languages'],
        education=data['education'],
        internship=data['internship'],
        experience=data['experience'],
        contact=data['contact'],
        certifications=data['certifications']
        
    )

    education_lines = data['education'].split('\n')
    experience_lines = data['experience'].split('\n')

    # Extract degree details
    degree, university, year_of_passing = extract_degree_details(education_lines)

    # Extract experience details
    designation, company_name, start_date, end_date = extract_experience_details(experience_lines)

    # Store education details in the database
    EducationDetails.objects.create(
        user_id_id=user_id,
        degree=degree,
        university=university,
        year_of_passing=year_of_passing
    )
    ExperienceDetails.objects.create(
        user_id_id=user_id,
        designation=designation,
        company_name=company_name,
        start_date=start_date,
        end_date=end_date
    )
    return ResumeDetails.objects.last()


def extract_degree_details(education_lines):
    degree = ""
    university = ""
    year_of_passing = ""
    degree_keywords = ["degree", "bachelor", "master", "diploma", "puc", "business", "Btech"]
    year_regex = r'\b\d{4}\b'
    for line in education_lines:
        match = re.search(year_regex, line)
        if match:
            year_of_passing = match.group()
            month_match = re.search(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', line, re.IGNORECASE)
            if month_match:
                year_of_passing += " " + month_match.group()
        elif any(keyword in line.lower() for keyword in degree_keywords):
            degree = line
        elif "college" in line.lower() or "university" in line.lower():
            university = line
    return degree, university, year_of_passing


def extract_experience_details(experience_lines):
    designation = ""
    company_name = ""
    start_date = ""
    end_date = ""
    designation_keywords = ["Executive Secretary", "Secretary", "Assistant", "software", "engineer", "analyst",
                            "agent", 'manager']
    company_keywords = ["pvt ltd", "Company", "limited", "corp"]
    date_regex = r'\b(?:\d{4}[-/]\d{2}[-/]\d{2}|\w+\s\d{4})\b'  # Matches YYYY-MM-DD, YYYY/MM/DD, MMM YYYY
    for line in experience_lines:
        if any(keyword in line for keyword in designation_keywords):
            designation = line.strip()
        if any(keyword in line for keyword in company_keywords):
            company_name = line.strip()
        match = re.search(date_regex, line)
        if match:
            if not start_date:
                start_date = match.group()
            else:
                end_date = match.group()
    return designation, company_name, start_date, end_date


def temp1(request):
    if request.method == 'POST':
        resume = request.FILES['resume']
        Resume.objects.create(resume_file=resume)
        resume_path = Resume.objects.last().resume_file.path
        resume_details = extract_and_store_resume_data(resume_path, request.user.id)
        context = {
            'resume_details': resume_details,
        }
        return render(request, 'temp1.html', context)
    return render(request, 'temp1.html')


def get_project_info(request):
    id=request.user.id
    latest_project = ResumeDetails.objects.filter(user_id=id).order_by('-id').first()
    if latest_project and latest_project.projects:
        project_info = {
            'project': latest_project.projects,
        }
    else:
        project_info = {
            'project': 'Add Your project',
        } 
    return JsonResponse(project_info) 

def get_languages_info(request):
    id=request.user.id
    latest_languages = ResumeDetails.objects.filter(user_id=id).order_by('-id').first()
    if latest_languages and latest_languages.languages:
        languages_info = {
            'languages': latest_languages.languages,
        }
    else:
        languages_info = {
            'languages': 'Add Languages',
        } 
    return JsonResponse(languages_info) 


    
def get_degree_info(request):
    id=request.user.id
    latest_education = EducationDetails.objects.filter(user_id=id).order_by('-id').first()
    if latest_education and latest_education.degree:
        degree_info = {
            'degree': latest_education.degree,
        }
    else:
        degree_info = {
            'degree': 'Add Your Degree Information',
        } 
    return JsonResponse(degree_info) 


def get_company_info(request):
    id=request.user.id
    latest_exp = ExperienceDetails.objects.filter(user_id=id).order_by('-id').first()
    if latest_exp and latest_exp.company_name:
        company_info = {
            'companyname': latest_exp.company_name,
        }
    else:
        company_info = {
            'companyname': 'Add company name',
        } 
    return JsonResponse(company_info) 



def get_first_name_info(request):
    id=request.user.id
    latest_fname = request.user.first_name
    print("!!!!!!!!!!!!!tttttttttttttttt",request.user.first_name)
    if latest_fname:
        fname_info = {
            'fname': latest_fname,
        }
    else:
        fname_info = {
            'fname': 'Add Name',
        } 
    return JsonResponse(fname_info) 

def get_last_name_info(request):
    id=request.user.id
    latest_lname = request.user.last_name
    if latest_lname:
        lname_info = {
            'lname': latest_lname,
        }
    else:
        fname_info = {
            'lname': ' ',
        } 

    return JsonResponse(lname_info) 

def get_email_info(request):
    id=request.user.id
    latest_email = request.user.email
    if latest_email:
        email_info = {
            'email': latest_email,
        }
    else:
        email_info = {
            'email': 'Add email',
        } 
    return JsonResponse(email_info) 

def get_phone_no_info(request):
    id=request.user.id
    latest_phone = request.user.phone_no
    if latest_phone:
        phone_info = {
            'phone_no': latest_phone,
        }
    else:
        phone_info = {
            'phone_no': 'Add contact number',
        } 
    return JsonResponse(phone_info) 

def get_linkedin_info(request):
    id=request.user.id
    latest_linkedin = request.user.linkedin
    if latest_linkedin:
        linkedin_info = {
            'linkedin': latest_linkedin,
        }
    else:
        linkedin_info = {
            'linkedin': 'Add linkedin url',
        } 
    return JsonResponse(linkedin_info) 

def get_designation_info(request):
    id=request.user.id
    latest_exp = ExperienceDetails.objects.filter(user_id=id).order_by('-id').first()
    if latest_exp and latest_exp.designation:
        des_info = {
            'designation': latest_exp.designation,
        }
    else:
        des_info = {
            'designation': 'Add designation',
        } 
    return JsonResponse(des_info) 

def get_university_info(request):
    id=request.user.id
    latest_education = EducationDetails.objects.filter(user_id=id).order_by('-id').first()
    if latest_education and latest_education.university:
        degree_info = {
            'university': latest_education.university,
        }
    else:
        degree_info = {
            'university': 'College name',
        } 
    return JsonResponse(degree_info) 

def get_skills_info(request):
    id=request.user.id
    skills = ResumeDetails.objects.filter(user_id=id).order_by('-id').first()
    if skills and skills.skills:
        skills_info = {
            'skills': skills.skills,
        }
    else:
        skills_info = {
            'skills': 'Add your skills',
        } 
    return JsonResponse(skills_info) 

def get_summary_info(request):
    id = request.user.id
    latest_summary = ResumeDetails.objects.filter(user_id=id).order_by('-id').first()
    if latest_summary and latest_summary.summary:
        summary_info = {
            'summary': latest_summary.summary,
        }
    else:
        summary_info = {
            'summary': 'Profile summary',
        } 
    return JsonResponse(summary_info)    

def temp4(request):
    if request.method == 'POST':
        # Process the uploaded resume file
        resume = request.FILES['resume']
        Resume.objects.create(resume_file=resume)
        resume_path = Resume.objects.last().resume_file.path
        # Extract and store resume data
        resume_details = extract_and_store_resume_data(resume_path, request.user.id)
        # Pass necessary data to the template context
        context = {
            'resume_details': resume_details,
            # Other context data if needed
        }
        return render(request, 'temp4.html', context)
    return render(request,'temp4.html')

def temp2(request):
    print("hhhhhhhhhhhhhhhhhh")
    if request.method == 'POST':
        # Process the uploaded resume file
        resume = request.FILES['resume']
        Resume.objects.create(resume_file=resume)
        resume_path = Resume.objects.last().resume_file.path
        # Extract and store resume data
        resume_details = extract_and_store_resume_data(resume_path, request.user.id)
        # Pass necessary data to the template context
        context = {
            'resume_details': resume_details,
            # Other context data if needed
        }
        return render(request, 'temp2.html', context)
    return render(request,'temp2.html')


def temp3(request):
    if request.method == 'POST':
        # Process the uploaded resume file
        resume = request.FILES['resume']
        Resume.objects.create(resume_file=resume)
        resume_path = Resume.objects.last().resume_file.path
        # Extract and store resume data
        resume_details = extract_and_store_resume_data(resume_path, request.user.id)
        # Pass necessary data to the template context
        context = {
            'resume_details': resume_details,
            # Other context data if needed
        }
        return render(request, 'temp3.html', context)
    return render(request,'temp3.html')

def temp6(request):
    if request.method == 'POST':
        # Process the uploaded resume file
        resume = request.FILES['resume']
        Resume.objects.create(resume_file=resume)
        resume_path = Resume.objects.last().resume_file.path
        # Extract and store resume data
        resume_details = extract_and_store_resume_data(resume_path, request.user.id)
        # Pass necessary data to the template context
        context = {
            'resume_details': resume_details,
            # Other context data if needed
        }
        return render(request, 'temp6.html', context)
    return render(request,'temp6.html')

def temp5(request):
    if request.method == 'POST':
        # Process the uploaded resume file
        resume = request.FILES['resume']
        Resume.objects.create(resume_file=resume)
        resume_path = Resume.objects.last().resume_file.path
        # Extract and store resume data
        resume_details = extract_and_store_resume_data(resume_path, request.user.id)
        # Pass necessary data to the template context
        context = {
            'resume_details': resume_details,
            # Other context data if needed
        }
        return render(request, 'temp5.html', context)
    return render(request,'temp5.html')

def temp7(request):
    if request.method == 'POST':
        # Process the uploaded resume file
        resume = request.FILES['resume']
        Resume.objects.create(resume_file=resume)
        resume_path = Resume.objects.last().resume_file.path
        # Extract and store resume data
        resume_details = extract_and_store_resume_data(resume_path, request.user.id)
        # Pass necessary data to the template context
        context = {
            'resume_details': resume_details,
            # Other context data if needed
        }
        return render(request, 'temp7.html', context)
    return render(request,'temp7.html')

def temp8(request):
    if request.method == 'POST':
        # Process the uploaded resume file
        resume = request.FILES['resume']
        Resume.objects.create(resume_file=resume)
        resume_path = Resume.objects.last().resume_file.path
        # Extract and store resume data
        resume_details = extract_and_store_resume_data(resume_path, request.user.id)
        # Pass necessary data to the template context
        context = {
            'resume_details': resume_details,
            # Other context data if needed
        }
        return render(request, 'temp8.html', context)
    return render(request,'temp8.html')

def temp9(request):
    return render(request,'temp9.html')


from django.core.files.storage import default_storage
def upload_image(request):
    if request.method == "POST":
        image = request.FILES.get('image_input')
        
        # Save the uploaded image using default storage
        image_path = default_storage.save('uploaded_images/' + image.name, image)
        
        # Get the URL of the uploaded image
        image_url = default_storage.url(image_path)
        
        # Return the URL as JSON response
        return JsonResponse({'image_url': image_url})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)