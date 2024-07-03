from django.views.decorators.csrf import csrf_exempt
import os
import tempfile
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .resume import extract_text_from_pdf, rnlp
from .job_des import extract_jdtext_from_pdf, jdnlp
from .serializers import ParsedResumeSerializer
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from .models import Parse  # Import the Parse model
from .models import Jd_ents  # Import the Parse model
import ast

# post request for resume parser

@csrf_exempt
@api_view(['POST','GET'])
def parse_resume(request):
    if request.method == 'POST':
        resume_file = request.FILES.get('resume')

        # Validate uploaded file
        if not isinstance(resume_file, UploadedFile):
            return JsonResponse({'error': 'Invalid file format'}, status=400)
        
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in resume_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        try:
            resume_text = extract_text_from_pdf(temp_file_path)
            doc = rnlp(resume_text)
            entities = [[ent.label_,ent.text] for ent in doc.ents]
        except Exception as e:
            # Handle parsing errors
            os.unlink(temp_file_path)  # Delete the temporary file
            return JsonResponse({'error': f'Error parsing resume: {str(e)}'}, status=500)

        os.unlink(temp_file_path)  # Delete the temporary file
        if entities:
    # Save extracted data to Parse model instance
    
            name = ""
            email= ""
            location = ""
            college_name = ""
            degree = ""
            companies = ""
            worked_as = ""
            skills = []
            experience = ""
            linkedin = ""
            
            for entity in entities:
                  if entity[0].lower() == 'name':
                      name = entity[1]
                  elif entity[0].lower() == 'email address':
                      email = entity[1]
                  elif entity[0].lower() == 'location':
                      location = entity[1]
                  elif entity[0].lower() == 'college name':
                      college_name = entity[1]
                  elif entity[0].lower() == 'degree':
                      degree = entity[1]  
                  elif entity[0].lower() == 'companies worked at':
                      companies = entity[1]
                  elif entity[0].lower() == 'worked as':
                      worked_as = entity[1]
                  elif entity[0].lower() == 'skills':
                      skills += entity[1].split(',')
                  elif entity[0].lower() == 'years of experience':
                      experience = entity[1]
                  elif entity[0].lower() == 'linkedin link':
                      linkedin = entity[1]
                  
            print("Name:", name)
            print("Email Address:", email)
            print("Location:", location)
            print("College Name:", college_name)
            print("Degree:", degree)
            print("Companies Worked At:", companies)
            print("Worked As :", worked_as)
            print("Skills:", skills)
            print("Years of experience:", experience)
            print("Linkedin Link:", linkedin)                       
            
        parse_instance = Parse.objects.create(name=name, email=email, location=location,college_name=college_name, degree=degree, companies = companies, worked_as=worked_as, skills=skills, experience=experience, linkedin=linkedin, extracted_data=entities)
            
        return JsonResponse({'success': 'Resume data extracted and saved successfully', 'id': parse_instance.id})
        
            
    else:
        return JsonResponse({'error': 'No entities found'}, status=400)
    

# get request for resume parser   
    

@csrf_exempt
@api_view(['GET'])   
def get_parsed_data(request):
    if request.method == 'GET':
        # Retrieve all stored parsed data
        parsed_data = Parse.objects.all()
        data_list = [{'id': item.id, 'name': item.name, 'email':item.email, 'location':item.location, 'college_name':item.college_name, 'degree':item.degree, 'companies':item.companies, 'worked_as':item.worked_as, 'skills':item.skills,  'experience':item.experience, 'linkedin':item.linkedin,  'extracted_data': item.extracted_data,} for item in parsed_data]

        print(data_list)
        return JsonResponse({'parsed_data': data_list})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    
    
    # Post request for jd parser
    
@csrf_exempt
@api_view(['POST','GET'])
def parse_jd(request):
    if request.method == 'POST':
        jd_file = request.FILES.get('jd')

        # Validate uploaded file
        if not isinstance(jd_file, UploadedFile):
            return JsonResponse({'error': 'Invalid file format'}, status=400)
        
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in jd_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        try:
            jd_text = extract_jdtext_from_pdf(temp_file_path)
            doc = jdnlp(jd_text)
            entities = [[ent.label_,ent.text] for ent in doc.ents]
        except Exception as e:
            # Handle parsing errors
            os.unlink(temp_file_path)  # Delete the temporary file
            return JsonResponse({'error': f'Error parsing resume: {str(e)}'}, status=500)

        os.unlink(temp_file_path)  # Delete the temporary file
        if entities:
    # Save extracted data to Parse model instance
    
            jobpost = ""
            degree = ""
            skills = []
            experience = ""
            
            for entity in entities:
                  if entity[0].lower() == 'jobpost':
                      jobpost = entity[1]
                  elif entity[0].lower() == 'degree':
                      degree = entity[1]
                  elif entity[0].lower() == 'skills':
                      skills += entity[1].split(',')
                  elif entity[0].lower() == 'experience':
                      experience = entity[1]                
                        
            print("Job Title:", jobpost)
            print("Degree:", degree)
            print("Skills:", skills)
            print("Years of experience:", experience)    

            
        jd_ents_instance = Jd_ents.objects.create( jobpost=jobpost, degree=degree, skills=skills, experience=experience, extracted_data=entities)
            
        return JsonResponse({'success': 'Job data extracted and saved successfully', 'id': jd_ents_instance.id})
        
            
    else:
        return JsonResponse({'error': 'No entities found'}, status=400)

@csrf_exempt
@api_view(['GET'])
def get_parsedjd_data(request):
    if request.method == 'GET':
        # Retrieve the latest stored parsed JD data
        try:
            latest_jd_ents = Jd_ents.objects.latest('created_at')
            data = {
                'id': latest_jd_ents.id,
                'jobpost': latest_jd_ents.jobpost,
                'degree': latest_jd_ents.degree,
                'skills': latest_jd_ents.skills,
                'experience': latest_jd_ents.experience,
                'extracted_data': latest_jd_ents.extracted_data,
            }
            return JsonResponse({'parsedjd_data': data})
        except Jd_ents.DoesNotExist:
            return JsonResponse({'error': 'No parsed JD data available'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    




@csrf_exempt
@api_view(['GET']) 
def get_ranked_resume(request):
 if request.method == 'GET':

    resume_data = Parse.objects.all()
    resume_entities = [{'resume_id': item.id, 'name': item.name, 'email':item.email, 'location':item.location, 'college_name':item.college_name, 'resume_degree':item.degree, 'resume_companies':item.companies, 'resume_worked_as':item.worked_as, 'resume_skills':item.skills,  'resume_experience':item.experience, 'linkedin':item.linkedin, 'extracted_data':item.extracted_data } for item in resume_data]

    jd_data = Jd_ents.objects.all()
    job_description_entities = [{'jd_id': item.id, 'required_degree': item.degree, 'jobpost':item.jobpost,'required_skills':item.skills,  'required_experience':item.experience, 'extracted_data': item.extracted_data,} for item in jd_data]

    print(resume_data)
    print(jd_data)


    def normalize_years_of_experience(experience):
        return float(experience.split()[0]) if experience else 0

    def normalize_skills(resume_skills, required_skills):
        resume_skills_lower = ast.literal_eval(resume_skills)
        required_skills_lower = ast.literal_eval(required_skills)
    
        matching_skills = 0
        for skill in resume_skills_lower:
            if skill in required_skills_lower:
                matching_skills += 1
        return matching_skills

    def normalize_degree(resume_degree, required_degree):
        return 1 if resume_degree.lower() in required_degree.lower() else 0

    def normalize_worked_as(resume_worked_as, jobpost):   
        return 1 if resume_worked_as.lower() in jobpost.lower() else 0
      
    def calculate_score(resume, job_description, weights):
        # Normalize data
        normalized_experience = normalize_years_of_experience(resume['resume_experience'])
        # print("Normalized Experience:", normalized_experience)
    
        normalized_skills = normalize_skills(resume['resume_skills'], job_description['required_skills'])
        # print("Normalized Skills:", normalized_skills)

        normalized_degree = normalize_degree(resume['resume_degree'],job_description['required_degree'])
        # print("Normalized Certification:", normalized_certification)

        normalized_worked_as = normalize_worked_as(resume['resume_worked_as'], job_description['jobpost'])
        # print("Normalized Worked As:", normalized_worked_as)

        # Calculate difference in experience
        required_experience = normalize_years_of_experience(job_description['required_experience'])
        experience_difference = normalized_experience - required_experience
        print("Experience Difference:", experience_difference)

        # Calculate scores
        score = (weights['experience'] * experience_difference) + (weights['skills'] * normalized_skills) + (weights['degree'] * normalized_degree) + (weights['worked_as'] * normalized_worked_as)
        print("Score:", score)
        return score

    def rank_resumes(resumes, job_descriptions, weights):
        ranked_resumes = []
        for resume in resumes:
         for job_description in job_descriptions:
            score = calculate_score(resume,job_description, weights)       
    
            
            ranked_resumes.append({'id': resume['resume_id'], 'name': resume['name'], 'email': resume['email'], 'score': score, 'jobpost': job_description['jobpost'],})
        ranked_resumes.sort(key=lambda x: x['score'], reverse=True)
        return ranked_resumes

    # Assigning wts.
    weights = {'experience': 0.3, 'skills': 0.4, 'degree': 0.05, 'worked_as': 0.25}

    # Rank resumes
    ranked_resumes = rank_resumes(resume_entities, job_description_entities, weights)

    # Print ranked resumes
    for i, resume in enumerate(ranked_resumes, 1):

        print(f"Rank {i}: Resume ID: {resume['id']}, Name:{resume['name']}, Email:{resume['email']}, Jobpost:{resume['jobpost']}, Score: {resume['score']}")
        
    return JsonResponse({'ranked_resumes': ranked_resumes}) 