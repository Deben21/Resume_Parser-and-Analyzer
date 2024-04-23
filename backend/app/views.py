from django.views.decorators.csrf import csrf_exempt
import os
import tempfile
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .resume import extract_text_from_pdf, nlp
from .job_des import extract_jdtext_from_pdf, nlp
from .serializers import ParsedResumeSerializer
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from .models import Parse  # Import the Parse model
from .models import Jd_ents  # Import the Parse model


# post request for resume parser
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
            doc = nlp(jd_text)
            entities = [[ent.label_,ent.text] for ent in doc.ents]
        except Exception as e:
            # Handle parsing errors
            os.unlink(temp_file_path)  # Delete the temporary file
            return JsonResponse({'error': f'Error parsing resume: {str(e)}'}, status=500)

        os.unlink(temp_file_path)  # Delete the temporary file
        if entities:
    # Save extracted data to Parse model instance
    
            education = ""
            worked_as = ""
            skills = []
            experience = ""
            
            for entity in entities:
                  if entity[0].lower() == 'education':
                      education = entity[1]
                  elif entity[0].lower() == 'worked as':
                      worked_as = entity[1]
                  elif entity[0].lower() == 'skills':
                      skills += entity[1].split(',')
                  elif entity[0].lower() == 'years of experience':
                      experience = entity[1]
                  
                  
        
            print("education:", education)
            print("Worked As :", worked_as)
            print("Skills:", skills)
            print("Years of experience:", experience)
            
            
                                
                
            
        jd_ents_instance = Jd_ents.objects.create( education=education, worked_as=worked_as, skills=skills, experience=experience, extracted_data=entities)
            
        return JsonResponse({'success': 'Data extracted and saved successfully', 'id': jd_ents_instance.id})
        
            
    else:
        return JsonResponse({'error': 'No entities found'}, status=400)

@csrf_exempt
@api_view(['GET'])   
def get_parsedjd_data(request):
    if request.method == 'GET':
        # Retrieve all stored parsed data
        parsedjd_data = Jd_ents.objects.all()
        data_list = [{'id': item.id, 'education': item.education, 'worked_as':item.worked_as,'skills':item.skills,  'experience':item.experience, 'extracted_data': item.extracted_data,} for item in parsedjd_data]

        print(data_list)
        return JsonResponse({'parsedjd_data': data_list})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

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
            doc = nlp(resume_text)
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
            
        return JsonResponse({'success': 'Data extracted and saved successfully', 'id': parse_instance.id})
        
            
    else:
        return JsonResponse({'error': 'No entities found'}, status=400)