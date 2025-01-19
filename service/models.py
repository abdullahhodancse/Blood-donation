from django.db import models

# Create your models here.
class service(models.Model):
    name=models.CharField(max_length=20)
    Description=models.TextField()
    Picture=models.ImageField(upload_to="service/Image/")

