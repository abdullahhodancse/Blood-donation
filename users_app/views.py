from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from .import models
from .import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
#for sanding email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from rest_framework.filters import SearchFilter
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response


class donerViewSet(viewsets.ModelViewSet):
    queryset = models.doner.objects.all()
    serializer_class = serializers.donerSerialaizers



class UserRegistrationApiView(APIView):
    serializer_class=serializers.RegistrationSerialaizers



    def post(self,request):
        serializer=self.serializer_class(data=request.data)
       
        if serializer.is_valid():
            user=serializer.save()
            token=default_token_generator.make_token(user)
            print("token",token)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            print("uid",uid)
            confirm_link=f"http://127.0.0.1:8000/doner/active/{uid}/{token}"
            email_subject="confirm Your Email"
            email_body=render_to_string('confirm_email.html',{'confirm_link':confirm_link
            
            })
            email=EmailMultiAlternatives(email_subject,'',to=[user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()

           
            return Response(" Check Your mail for Cnfirmation")
        return Response(serializer.errors)





def activate(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user=None


    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        return redirect('login') 
    else:
         return redirect('register') 

class UserLoginView(APIView):
    def post(self,request):
        serializer=serializers.UserLogInSerializers(data=self.request.data)
        if serializer.is_valid():
            username= serializer.validated_data['username']
            password= serializer.validated_data['password']

            user=authenticate(username=username,password=password)
            if user:
                # token=Token.objects.get_or_create(user=user)
                token, _ = Token.objects.get_or_create(user=user)
                print(_)
                login(request, user)
                return Response({'token':token.key,'user_id':user.id})
            else:
                return Response({'error':"Invalite"})   
                     
        return Response(serializer.error)


# class UserLogOutView(APIView):
#     def get(self,request):
#         request.user.auth_token.delete()
#         logout(request)
#         return redirect('login')


class Blood_Group_ViewSet(viewsets.ModelViewSet):
    queryset = models.BloodGroup.objects.all()
    serializer_class = serializers.blood_group_Serialaizers


class request_accept_ViewSet(viewsets.ModelViewSet):
    queryset = models.BloodRequestAcceptance.objects.all()
    serializer_class = serializers.BloodRequestAcceptanceSerializer
    

class UserLogOutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')

# class BloodRequestViewSet(viewsets.ModelViewSet):
#     queryset =  models.BloodRequest.objects.all()
#     serializer_class = serializers.BloodRequestSerializer
   

#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)

#     @action(detail=True, methods=['post'])
#     def accept(self, request, pk=None):
#         blood_request = self.get_object()
#         try:
#             donor = models.doner.objects.get(user=request.user)
#         except models.doner.DoesNotExist:
#             return Response({'error': 'You must be a registered donor to accept a request.'}, status=400)

#         # Check if the logged-in user is the one who created the request
#         if blood_request.created_by.id == request.user.id:
#             return Response({'error': 'You cannot accept your own request!'}, status=400)

#         # Check if the request has already been accepted by someone else
#         if blood_request.accepted_by is not None:
#             return Response({'error': 'This request is already accepted by someone else!'}, status=400)
#         blood_request.accepted_by = request.user
#         blood_request.is_completed = True
#         blood_request.save()
        
#         DonationHistory.objects.create(
#             donor=request.user,
#             recipient=blood_request.created_by,
#             blood_request=blood_request,
#             status='Donated'
#         )
        
#         return Response({'message': 'Blood donation request accepted successfully!'})



class BloodRequestViewSet(viewsets.ModelViewSet):
    queryset = models.BloodRequest.objects.all()
    serializer_class = serializers.BloodRequestSerializer
    # permission_classes = [IsAuthenticated]  # Only logged-in users can post a request

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """
        Only registered donors can accept a request.
        """
        blood_request = self.get_object()
        user = request.user

        # Check if user is a donor
        donor = models.doner.objects.filter(user=user).first()
        if not doner:
            return Response({"error": "Only registered donors can accept requests."}, status=status.HTTP_403_FORBIDDEN)

        # Check if request is already accepted
        if blood_request.is_completed:
            return Response({"error": "This request has already been accepted."}, status=status.HTTP_400_BAD_REQUEST)

        # Prevent requesters from accepting their own requests
        if blood_request.created_by == user:
            return Response({"error": "You cannot accept your own request."}, status=status.HTTP_400_BAD_REQUEST)

        # Accept the request
        acceptance = BloodRequestAcceptance.objects.create(
            blood_request=blood_request,
            accepted_by=donor
        )

        # Mark request as completed
        blood_request.is_completed = True
        blood_request.save()

        return Response({"message": "Blood request accepted successfully!"}, status=status.HTTP_200_OK)