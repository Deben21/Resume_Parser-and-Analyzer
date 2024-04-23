from django.db import models
# Create your models here.
class Parse(models.Model):
    name = models.CharField(max_length= 255)
    email = models.EmailField(default='Unknown')
    location = models.CharField(max_length= 255)
    college_name = models.CharField(max_length=255)
    degree = models.CharField(max_length= 255)
    companies = models.CharField(max_length= 255)
    worked_as = models.CharField(max_length= 255)
    skills = models.CharField(max_length= 500)
    experience = models.CharField(max_length= 255)
    linkedin = models.URLField(blank=True, null=True)
    extracted_data = models.TextField(blank = True)

class Jd_ents(models.Model):
    education = models.CharField(max_length= 255)
    worked_as = models.CharField(max_length= 255)
    skills = models.CharField(max_length= 500)
    experience = models.CharField(max_length= 255)
    extracted_data = models.TextField(blank = True)

    def __str__(self):
        return self.education

