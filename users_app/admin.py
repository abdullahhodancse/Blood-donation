from django.contrib import admin
from .models import doner,BloodGroup,BloodRequest
from .import models

# Register your models here.
class doneradmin(admin.ModelAdmin):
    list_display=['id','first_name','Mobile_number','image','city','Street','other','date_bath','is_available']



    def first_name(self,obj):
        return obj.user.first_name

    def last_name(self,obj):
        return obj.user.last_name     


class BloodGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class blood_request_admin(admin.ModelAdmin):
    list_display=['created_by', 'blood_group', 'hospital_name', 'location', 'request_date', 'is_completed']

class blood_request_accept_admin(admin.ModelAdmin):
    list_display=['blood_request','accepted_by','acceptance_date']


admin.site.register(models.BloodRequest,blood_request_admin)
admin.site.register(models.BloodRequestAcceptance,blood_request_accept_admin)
admin.site.register(models.doner,doneradmin)
admin.site.register(models.BloodGroup,BloodGroupAdmin)






