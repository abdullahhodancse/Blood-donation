from django.shortcuts import render


from rest_framework import viewsets

# Create your views here.
from .import models
from .import serializers

class ServicesViewSet(viewsets.ModelViewSet):
    queryset = models.service.objects.all()
    serializer_class = serializers.ServicesSerialaizers