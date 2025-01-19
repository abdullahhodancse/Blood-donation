from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now




class BloodGroup(models.Model):
    name=models.CharField(max_length=30)
    slug=models.SlugField(max_length=30)

    def __str__(self):
        return self.name 


class doner(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Mobile_number=models.CharField(max_length=12)
    age = models.PositiveIntegerField()
    blood_group=models.ForeignKey(BloodGroup,on_delete=models.CASCADE,default=1)
    city=models.CharField(max_length=120)
    Street=models.CharField(max_length=120)
    other=models.TextField()
    date_bath=models.DateField()
    last_donation_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)  

    image=models.ImageField(upload_to='patient/images/')
    




    def __str__(self):
        return f"{self.user.username} "


class BloodRequest(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    # blood_group = models.CharField(max_length=5)
    blood_group=models.ForeignKey(BloodGroup,on_delete=models.CASCADE,default=1)
    hospital_name = models.CharField(max_length=255)
    location = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
  
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Blood Request by {self.created_by.username} for {self.blood_group}"


class BloodRequestAcceptance(models.Model):
    blood_request = models.OneToOneField(BloodRequest, on_delete=models.CASCADE)
    accepted_by = models.OneToOneField(doner, on_delete=models.CASCADE)
    acceptance_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
      
        self.blood_request.is_completed = True
        self.blood_request.save()

        if self.accepted_by:
            self.accepted_by.is_available = False
            self.accepted_by.save()
           

        super().save(*args, **kwargs) 
    def __str__(self):
        return f"{self.accepted_by.user.username}"