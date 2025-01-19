from django.db import models

# Create your models here.
class ContactUs(models.Model):
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    problem=models.TextField()

    def __str__(self):
        return self.Name

    
    
