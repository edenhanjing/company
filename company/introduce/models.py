from django.db import models

# Create your models here.

class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    introduce = models.TextField()
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    company_logo = models.ImageField(upload_to='CompanLogo',blank=True,default='CompanLogo/default.png')

    def __str__(self):
        return self.company_name


class Department(models.Model):
    department_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    introduce = models.TextField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    company = models.ForeignKey('CompanyInfo',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.department_name
